import logging
import voluptuous as voluptuous

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.core import callback

from homeassistant.const import (
    TEMP_CELSIUS,
    CONF_MAC,
    CONF_SENSORS,
    ATTR_FRIENDLY_NAME
)

from bluepy import btle, thingy52
from datetime import timedelta
import binascii
import time

VERSION = '0.1.0'
CONNECTED = 'conn'
DISCONNECTED = 'disc'

_LOGGER = logging.getLogger(__name__)

# Definition of all UUID used by Thingy
CCCD_UUID = 0x2902
RETRY_INTERVAL_SEC = 5

CONF_GAS_INT = 'gas_interval'
CONF_REFRESH_INT = 'refresh_interval'

DEFAULT_NAME = 'Thingy:'
DEFAULT_REFRESH_INTERVAL = timedelta(seconds=60)
DEFAULT_GAS_INTERVAL = 3

# Sensor types are defined like: Name, units, icon
SENSOR_TYPES = {
    "humidity": ['Humidity', '%', 'mdi:water-percent'],
    "temperature": ['Temperature', TEMP_CELSIUS, 'mdi:thermometer'],
    "co2": ['Carbon Dioxide', 'ppm', 'mdi:periodic-table-co2'],
    "tvoc": ['Air Quality', 'ppb', 'mdi:air-filter'],
    "pressure": ['Atmospheric Pressure', 'hPA', 'mdi:gauge'],
    "battery": ["Battery Level", "%", "mdi:battery-50"]
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string,
    vol.Optional(ATTR_FRIENDLY_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_REFRESH_INT,
                 default=DEFAULT_REFRESH_INTERVAL): cv.time_period,
    vol.Optional(CONF_GAS_INT, default=DEFAULT_GAS_INTERVAL): cv.positive_int,
    vol.Optional(CONF_SENSORS, default=list(SENSOR_TYPES)): vol.All(
            cv.ensure_list, [vol.In(SENSOR_TYPES)]
        ),
})

async def async_setup_platform(hass, config,
                               async_add_entities, discovery_info=None):
    """ Set up the Thingy 52 sensors"""
    backend = BACKEND
    _LOGGER.debug('Version %s', VERSION)
    _LOGGER.info('if you have ANY issues with this, please report them here:'
                 ' https://github.com/kflinderman/Hassio/')
    _LOGGER.debug("Thingy52 is using %s backend.", backend.__name__)

    refresh_interval = config.get(CONF_REFRESH_INT).total_seconds()
    gas_interval = config.get(CONF_GAS_INT)

    mainConnection = setupThingy(
        config.get(CONF_MAC),
        refresh_interval,
        gas_interval,
        config[CONF_SENSORS]
    )

    devs = []

    for paramter in config[CONF_SENSORS]:
        name = SENSOR_TYPES[parameter][0]
        unit = SENSOR_TYPES[parameter][1]
        icon = SENSOR_TYPES[parameter][2]

        friendly_name = config.get(ATTR_FRIENDLY_NAME)
        if friendly_name:
            name = f"{friendly_name} {name}"

        devs.append(
            Thingy52Sensor(mainConnection, parameter, name, unit, icon)
        )

    async_add_entities(devs)
    mainConnection.devices = devs
    mainConnection.setDel()


class setupThingy:
    def __init__(self, mac_address, refresh_interval, gas_interval, sensors):
        self.mac = mac_address
        self.refresh_interval = refresh_interval
        self.notifications = int(refresh_interval) * 1000
        self.gas_interval = gas_interval
        self.conf_sensors = sensors
        self.thingy52 = None
        self.devices = None

    def connect(self):
        try:
            self.thingy52 = thingy52.Thingy(self.mac)
        except Exception as e:
            _LOGGER.debug("#[THINGYSENSOR]: Unable to connect to Thingy: %s",
                          str(e))
            return

        _LOGGER.debug("#[THINGYSENSOR]: Enabling environment")
        global e_battery_handle
        self.thingy52.environment.enable()

        if "temperature" in self.conf_sensors:
            self.thingy52.environment.set_temperature_notification(True)
            self.thingy52.environment.configure(temp_int=self.notifications)
        if "humidity" in self.conf_sensors:
            self.thingy52.environment.set_humidity_notification(True)
            self.thingy52.environment.configure(humid_int=self.notifications)
        if (("co2" in self.conf_sensors) or ("tvoc" in self.conf_sensors)):
            self.thingy52.environment.set_gas_notification(True)
            self.thingy52.environment.configure(gas_mode_int=self.gas_interval)
        if "pressure" in self.conf_sensors:
            self.thingy52.environment.set_pressure_notification(True)
            self.thingy52.environment.configure(press_int=self.notifications)
        if "battery" in self.conf_sensors:
            self.thingy52.battery.enable()
            """Battery notification not included in bluepy.thingy52"""
            e_battery_handle = self.thingy52.battery.data.getHandle()
            batt_ccd = self.thingy52.battery.data.getDescriptors(forUUID=CCCD_UUID)[0]
            batt_ccd.write(b"\x01\x00", True)

        return self.thingy52

    def setDel(self):
        _LOGGER.debug("#[THINGYSENSOR]: Enabling delegate")
        self.thingy52.withDelegate(NotificationDelegate(self.devices))

    def disconnect(self):
        if "temperature" in self.conf_sensors
            self.thingy52.environment.set_temperature_notification(False)
        if "humidity" in self.conf_sensors:
            self.thingy52.environment.set_humidity_notification(False)
        if (("co2" in self.conf_sensors) or ("tvoc" in self.conf_sensors)):
            self.thingy52.environment.set_gas_notification(False)
        if "pressure" in self.conf_sensors:
            self.thingy52.environment.set_pressure_notification(False)
            
        self.thingy52.disconnect()
        del self.thingy52


class Thingy52Sensor(Entity):
    def __init__(self, thingy, parameter, name, unit, icon):
        self.thingy = thingy
        self.parameter = parameter
        self._unit = unit
        self._icon = icon
        self._name = name
        self._state = None
        self._available = False

    async def async_added_to_hass(self):
        """Set initial state."""

        @callback
        def on_startup(_):
            self.async_schedule_update_ha_state(True)

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, on_startup)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def unit_of_measurement(self):
        """Return the units of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if "battery" in self._name and self._state is not None:
            return icon_for_battery_level(
                battery_level=int(self._state), charging=False
            )
        return self._icon

    def update(self):
        if CONNECTED in self.thingy.getState():
            try:
                _LOGGER.debug("#[%s]: Update", self._name)
                self.thingy.waitForNotifications(timeout=5)
            except Exception as e:
                _LOGGER.debug("#[%s]: method did not update: %s",
                              self._name, str(e))
                if "disconnected" in str(e):
                    self._available = False
                    self.thingy.disconnect()
                    return

            _LOGGER.debug("#[%s]: method update, state is %s",
                          self._name, self._state)
            self._available = True
        else:
            self.thingy.connect()


class NotificationDelegate(btle.DefaultDelegate):
    """ Custom delegate class to handle notifications from the Thingy:52 """
    def __init__(self, sensors):
        self.thingysensors = {}
        for s in sensors:
            self.thingysensors[s._name] = s

    def handleNotification(self, hnd, data):
        _LOGGER.debug("# [THINGYSENSOR]: Got notification - %s (%s)",
                      hnd, data)
        if (hnd == thingy52.e_temperature_handle):
            teptep = binascii.b2a_hex(data)
            tempinteg = self._str_to_int(teptep[:-2])
            tempdec = int(teptep[-2:], 16)

            div = 100 if((int(teptep[-2:], 16) / 10) > 1.0) else 10
            self.thingysensors["temperature"]._state = (tempinteg +
                                                        (tempdec / div))

        elif (hnd == thingy52.e_humidity_handle):
            teptep = binascii.b2a_hex(data)
            self.thingysensors["humidity"]._state = self._str_to_int(teptep)

        elif (hnd == thingy52.e_pressure_handle):
            pressure_int, pressure_dec = self._extract_pressure_data(data)
            div = 100 if((pressure_dec / 10) > 1.0) else 10
            self.thingysensors["pressure"]._state = (pressure_int +
                                                     (pressure_dec/div))

        elif (hnd == thingy52.e_gas_handle):
            eco2, tvoc = self._extract_gas_data(data)
            if ("co2" in self.thingysensors):
                if(eco2 != 0):
                    self.thingysensors["co2"]._state = eco2
            if ("tvoc" in self.thingysensors):
                self.thingysensors["tvoc"]._state = tvoc

        elif (hnd == e_battery_handle):
            teptep = binascii.b2a_hex(data)
            self.thingysensors["battery"]._state = int(teptep, 16)

    def _extract_pressure_data(self, data):
        """ Extract pressure data from data string. """
        teptep = binascii.b2a_hex(data)
        pressure_int = 0
        for i in range(0, 4):
            pressure_int += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
        pressure_dec = int(teptep[-2:], 16)
        return (pressure_int, pressure_dec)

    def _extract_gas_data(self, data):
        """ Extract gas data from data string. """
        teptep = binascii.b2a_hex(data)
        eco2 = int(teptep[:2], 16) + (int(teptep[2:4], 16) << 8)
        tvoc = int(teptep[4:6], 16) + (int(teptep[6:8], 16) << 8)
        return eco2, tvoc

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i
