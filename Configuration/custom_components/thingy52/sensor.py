"""
    HomeAssistant: Thingy52 temperature sensor
    Author: @chriswils

    This sensor device is taking data from the Nordic Thingy:52 IoT Sensor Platform.
    It is derived from HA example sensor; https://home-assistant.io/developers/platform_example_sensor/
    and uses bluepy's Thingy:52 implementation. More docs on this and snippets used in this file is 
    found at Nordic Semiconductor's devzone blog:
    https://devzone.nordicsemi.com/blogs/1162/nordic-thingy52-raspberry-pi-python-interface/
    
"""

import voluptuous as vol
from homeassistant.const import (
    TEMP_CELSIUS, 
    CONF_MAC, 
    CONF_SENSORS, 
    ATTR_FRIENDLY_NAME
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA
from bluepy import btle, thingy52
from datetime import timedelta
import binascii
import logging
import time

# DEPENDENCIES = ['libglib2.0-dev']
# REQUIREMENTS = ['bluepy']

VERSION = '0.1.0'

_LOGGER = logging.getLogger(__name__)

# Definition of all UUID used by Thingy
CCCD_UUID = 0x2902
RETRY_INTERVAL_SEC = 5

CONF_GAS_INT = 'gas_interval'
CONF_REFRESH_INT = 'refresh_interval'

CONNECTED = 'conn'
DISCONNECTED = 'disc'

DEFAULT_NAME = 'Thingy:'
DEFAULT_REFRESH_INTERVAL = timedelta(seconds=60)
DEFAULT_GAS_INTERVAL = 3

SENSOR_TYPES = {
    "humidity": ['Humidity', '%', 'mdi:water-percent'],
    "temperature" : ['Temperature', TEMP_CELSIUS, 'mdi:thermometer'],
    "co2": ['Carbon Dioxide', 'ppm', 'mdi:periodic-table-co2'],
    "tvoc": ['Air Quality', 'ppb', 'mdi:air-filter'],
    "pressure": ['Atmospheric Pressure', 'hPA', 'mdi:gauge'],
    "battery": ["Battery Level", "%", "mdi:battery-50"]
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string,
    vol.Optional(ATTR_FRIENDLY_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_REFRESH_INT, default=DEFAULT_REFRESH_INTERVAL): cv.time_period,
    vol.Optional(CONF_GAS_INT, default=DEFAULT_GAS_INTERVAL): cv.positive_int,
    vol.Required(CONF_SENSORS, default=[]): vol.All(
            cv.ensure_list, [vol.In(SENSOR_TYPES)]
        ),
})

""" Custom delegate class to handle notifications from the Thingy:52 """
class NotificationDelegate(btle.DefaultDelegate):
    def __init__(self, sensors):
        self.thingysensors = {}
        for s in sensors:
            self.thingysensors[s._name] = s

    def handleNotification(self, hnd, data):
        _LOGGER.debug("# [THINGYSENSOR]: Got notification")
        if (hnd == thingy52.e_temperature_handle):
            teptep = binascii.b2a_hex(data)
            tempinteg = self._str_to_int(teptep[:-2])
            tempdec = int(teptep[-2:], 16)

            div = 100 if((int(teptep[-2:], 16) / 10) > 1.0) else 10
            self.thingysensors["temperature"]._state = (tempinteg + (tempdec / div))   
        
        elif (hnd == thingy52.e_humidity_handle):
            teptep = binascii.b2a_hex(data)
            self.thingysensors["humidity"]._state = self._str_to_int(teptep)

        elif (hnd == thingy52.e_pressure_handle):
            pressure_int, pressure_dec = self._extract_pressure_data(data)
            div = 100 if( (pressure_dec / 10) > 1.0) else 10
            self.thingysensors["pressure"]._state = pressure_int + (pressure_dec/div)

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

class localThingy:
    def __init__(self, mac_address, conf_sensors, friendly_name, refresh_interval, gas_interval, notification_interval):
        self.mac = mac_address
        self.conf_sensors = conf_sensors
        self.friendly_name = friendly_name
        self.refresh_interval = refresh_interval
        self.gas_interval = gas_interval
        self.notification_interval = notification_interval
        self.thingy = None
        self.sensors = None
        self.available = None
        self.environment_set = False
        self.delegate_set = False
        self.first_time = True
        self.connecting = False
        
    def connect(self):
        self.connecting = True
        try:
            self.thingy = thingy52.Thingy52(self.mac)
            self.available = True
            _LOGGER.debug("#[THINGYSENSOR]: Connected")
            
            if not self.environment_set:
                self.environmental()
        except Exception as e:
            _LOGGER.debug("#[THINGYSENSOR]: Unable to connect to Thingy: %s", str(e))
            self.available = False
            
        self.connecting = False
        return self.thingy
        
    def setDel(self):
        self.thingy.setDelegate(NotificationDelegate(self.sensors))
        self.delegate_set = True
        
    def environmental(self):
        _LOGGER.debug("#[THINGYSENSOR]: Enabling environment notifications")
        global e_battery_handle
        self.thingy.environment.enable()

        # Enable notifications for enabled services
        # Update interval 1000ms = 1s
        if "temperature" in self.conf_sensors:
            self.thingy.environment.set_temperature_notification(True)
            self.thingy.environment.configure(temp_int=self.notification_interval)
        if "humidity" in self.conf_sensors:
            self.thingy.environment.set_humidity_notification(True)
            self.thingy.environment.configure(humid_int=self.notification_interval)
        if ( ("co2" in self.conf_sensors) or ("tvoc" in self.conf_sensors) ):
            self.thingy.environment.set_gas_notification(True)
            self.thingy.environment.configure(gas_mode_int=self.gas_interval)
        if "pressure" in self.conf_sensors:
            self.thingy.environment.set_pressure_notification(True)
            self.thingy.environment.configure(press_int=self.notification_interval)
        if "battery" in self.conf_sensors:
            self.thingy.battery.enable()
            # Battery notification not included in bluepy.thingy52
            e_battery_handle = self.thingy.battery.data.getHandle() # Is this needed?
            battery_ccd = self.thingy.battery.data.getDescriptors(forUUID=CCCD_UUID)[0]
            battery_ccd.write(b"\x01\x00", True)
            
        self.environment_set = True
        
        if not self.delegate_set and not self.first_time:
            self.setDel()
    
def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Set up the Thingy 52 temperature sensor"""
    
    _LOGGER.debug('Version %s', VERSION)
    _LOGGER.info('if you have ANY issues with this, please report them here:'
                 ' https://github.com/wlgrd/thingy52_homeassistant')

    mac_address = config.get(CONF_MAC)
    conf_sensors = config.get(CONF_SENSORS)
    friendly_name = config.get(ATTR_FRIENDLY_NAME)
    refresh_interval = config.get(CONF_REFRESH_INT)
    gas_interval = config.get(CONF_GAS_INT)
    
    refresh_interval = refresh_interval.total_seconds()
    notification_interval = int(refresh_interval) * 1000
    
    sensors = []
    """
    _LOGGER.debug("#[THINGYSENSOR]: Connecting to Thingy %s with address %s", friendly_name, mac_address[-6:])
    try:
        thingy = thingy52.Thingy52(mac_address)
    except Exception as e:
        _LOGGER.error("#[THINGYSENSOR]: Unable to connect to Thingy (%s): %s", friendly_name, str(e))
    """
    thingyInstance = localThingy(mac_address, conf_sensors, friendly_name, refresh_interval, gas_interval, notification_interval)
    _LOGGER.debug("#[THINGYSENSOR]: Connecting")
    thingy = thingyInstance.connect()

    # _LOGGER.debug("#[THINGYSENSOR]: Configuring and enabling environment notifications")
    # thingy.environment.enable()

    # # Enable notifications for enabled services
    # # Update interval 1000ms = 1s
    # if "temperature" in conf_sensors:
        # thingy.environment.set_temperature_notification(True)
        # thingy.environment.configure(temp_int=notification_interval)
    # if "humidity" in conf_sensors:
        # thingy.environment.set_humidity_notification(True)
        # thingy.environment.configure(humid_int=notification_interval)
    # if ( ("co2" in conf_sensors) or ("tvoc" in conf_sensors) ):
        # thingy.environment.set_gas_notification(True)
        # thingy.environment.configure(gas_mode_int=gas_interval)
    # if "pressure" in conf_sensors:
        # thingy.environment.set_pressure_notification(True)
        # thingy.environment.configure(press_int=notification_interval)
    # if "battery" in conf_sensors:
        # thingy.battery.enable()
        # # Battery notification not included in bluepy.thingy52
        # e_battery_handle = thingy.battery.data.getHandle() # Is this needed?
        # battery_ccd = thingy.battery.data.getDescriptors(forUUID=CCCD_UUID)[0]
        # battery_ccd.write(b"\x01\x00", True)


    for sensorname in conf_sensors:
        _LOGGER.debug("Adding sensor: %s", sensorname)
        sensors.append(Thingy52Sensor(thingy, sensorname, SENSOR_TYPES[sensorname][0],
                                      friendly_name, SENSOR_TYPES[sensorname][1], SENSOR_TYPES[sensorname][2], mac_address, thingyInstance))
    
    add_devices(sensors)
    thingyInstance.sensors = sensors
    thingyInstance.first_time = False
    if thingyInstance.available:
        thingyInstance.setDel()

class Thingy52Sensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, thingy, name, sensor_name, friendly_name, unit_measurement, icon, mac, instance):
        """Initialize the sensor."""
        self._thingy = thingy
        self._name = name
        self._sensor_name = sensor_name
        self._friendly_name = friendly_name
        self._state = None
        self._icon = icon
        self._unit_measurement = unit_measurement
        self._mac = mac
        self._instance = instance


    @property
    def name(self):
        """Return the name of the sensor."""
        return ("{} {}".format(self._friendly_name, self._sensor_name))

    @property
    def available(self):
        """Return True if available."""
        return self._instance.available
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
        
    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self._name == "battery" and self._state is not None:
            return icon_for_battery_level(
                battery_level=int(self._state), charging=False
            )
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_measurement

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("#[%s]: Update", self._name)
        if not self._instance.available:
            _LOGGER.debug("#[%s]: Not available, try to reconnect", self._name)
            try:
                if not self._instance.connecting:
                    self._thingy = self._instance.connect()
                    self._instance.available = True
            except Exception as e:
                _LOGGER.debug("#[%s]: method did not update - disconnected: %s", self._name, str(e))
                
        if self._instance.available:
            _LOGGER.debug("#[%s]: Available, wait for notification", self._name)
            try:
                self._thingy.waitForNotifications(timeout=5)
                _LOGGER.debug("#[%s]: method update, state is %s", self._name, self._state)
            except Exception as e:
                # if "disconnected" in str(e):
                _LOGGER.debug("#[%s]: method did not update - connected: %s", self._name, str(e))
                self._instance.available = False
        

if (__name__ == "__main__"):
    setup_platform()