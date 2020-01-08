# Home Assistant Configuration
This is my primary [Home Assistant](https://home-assistant.io/) configuration, This instance is running 0.101.3 on a Raspberry Pi 3B+ with the [HassOS](https://github.com/home-assistant/hassos) operating system runn HassIO.  It was installed [following this guide](https://www.home-assistant.io/hassio/installation/).

## Structure
* [AppDaemon](https://github.com/hassio-addons/addon-appdaemon3)
* [Configurator](https://www.home-assistant.io/addons/configurator/)
* [DuckDNS](https://www.home-assistant.io/addons/duckdns/)
* [Emulated Hue](https://www.home-assistant.io/integrations/emulated_hue/)
* [Grafana](https://github.com/hassio-addons/addon-grafana)
* [InfuxDB](https://github.com/hassio-addons/addon-influxdb)
* [Let's Encrypt](https://www.home-assistant.io/addons/lets_encrypt/)
* [MariaDB](https://www.home-assistant.io/addons/mariadb/)
* [Mosquitto](https://www.home-assistant.io/docs/mqtt/)
* [SSH & Web Terminal](https://github.com/hassio-addons/addon-ssh)
* [Z-Wave](https://www.home-assistant.io/docs/z-wave/) - [Z-Stick Gen 5](https://aeotec.com/z-wave-usb-stick/)

## Integrations, Devices, and Services
Here is a list of all of the devices and services that I use.  I will link to each integration.  I will also indicated which ones require purchasing an item, I'll do this because I'm always surprised about what is available to make your home smart that is readily available for free.  I have not included everything here, because some are custom integrations which I will discuss separately.

### Cameras
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [Amcrest](https://amcrest.com/) | [Link](https://www.home-assistant.io/integrations/amcrest/) | Yes | [IP3M-943B](https://amcrest.com/amcrest-3mp-bullet-wifi-video-security-ip-camera-pt-ip3m-943b.html) | |
| [Amcrest](https://amcrest.com/) | [Link](https://www.home-assistant.io/integrations/amcrest/) | Yes | [IP2M-841B](https://amcrest.com/amcrest-1080p-wifi-video-security-ip-camera-pt.html) | |
| [SkyBell](http://www.skybell.com/) | [Link](https://www.home-assistant.io/integrations/skybell/) | Yes | [SkyBell Trim Plus](http://www.skybell.com/product/skybell-video-doorbell-trim-plus/) | |

### Device Trackers
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [GPSLogger](http://gpslogger.app/) | [Link](https://www.home-assistant.io/integrations/gpslogger/) | No | [GPSLogger App](https://play.google.com/store/apps/details?id=com.mendhak.gpslogger) | |
| Home Assistant Bluetooth | [Link](https://www.home-assistant.io/integrations/bluetooth_tracker/) | No | | |
| Home Assistant IOS | [Link](https://companion.home-assistant.io/) | No | [Home Assistant Companion](https://apps.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401) | |
| Home Assistant Android | [Link](https://companion.home-assistant.io/) | No | [Home Assistant](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android) | |
| [Netgear](https://www.netgear.com/default.aspx) | [Link](https://www.home-assistant.io/integrations/netgear/) | Yes | [Netgear R7000](https://www.netgear.com/home/products/networking/wifi-routers/R7000.aspx) | Currently not functioning correctly.  It does not update status correctly and is often unreliable | 

### HVAC
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [Ecobee](https://www.ecobee.com/) | [Link](https://www.home-assistant.io/integrations/ecobee/) | Yes | [Ecobee3](https://www.ecobee.com/ecobee3/) | |

### Lights
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [Philips Hue](https://www2.meethue.com/en-us) | [Link](https://www.home-assistant.io/integrations/hue/) | Yes | [Color](https://www2.meethue.com/en-us/p/hue-white-and-color-ambiance-1-pack-e26/046677548483) | |
| [Philips Hue](https://www2.meethue.com/en-us) | [Link](https://www.home-assistant.io/integrations/hue/) | Yes | [White](https://www2.meethue.com/en-us/p/hue-white-single-bulb-e26/046677530341) | |

### Media Players
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [Google Play Music Desktop Player](https://www.googleplaymusicdesktopplayer.com/) | [Link](https://www.home-assistant.io/integrations/gpmdp/) | No | | |
| [LG Netcast](https://www.lg.com/us/tvs) | [Link](https://www.home-assistant.io/integrations/lg_netcast/) | Yes | [LG 42in Smart TV](https://www.lg.com/us/support/product/lg-42LM6200.AUS) | Can only power off the TV and display a non refreshing screenshot of the image |
| [Yamaha AVR](https://usa.yamaha.com/products/audio_visual/av_receivers_amps/index.html) | [Link](https://www.home-assistant.io/integrations/yamaha/) | Yes | [RX-V671](https://usa.yamaha.com/products/audio_visual/av_receivers_amps/rx-v671/index.html) | |
| [Yamaha AVR](https://usa.yamaha.com/products/audio_visual/av_receivers_amps/index.html) | [Link](https://www.home-assistant.io/integrations/yamaha/) | Yes | [RX-V683](https://usa.yamaha.com/products/audio_visual/av_receivers_amps/rx-v683_u/index.html) | |

### Notifications
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| Home Assistant IOS | [Link](https://www.home-assistant.io/docs/ecosystem/ios/) | No | [Home Assistant Companion](https://apps.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401) | |
| [Pushbullet](https://www.pushbullet.com/) | [Link](https://www.home-assistant.io/integrations/pushbullet/) | No | [Pushbullet Apps](https://www.pushbullet.com/apps) | |

### Other
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [IFTTT](https://ifttt.com/) | [Link](https://www.home-assistant.io/integrations/ifttt/) | No | [IFTTT App](https://play.google.com/store/apps/details?id=com.ifttt.ifttt&hl=en_US) | |
| N/A | N/A | Yes | [Lutron Aurora](http://www.lutron.com/en-US/Products/Pages/StandAloneControls/Dimmers-Switches/SmartBulbDimmer/overview.aspx) | Used so people stop turning off Hue bulbs |

### PC Control
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| RPC Shutdown | [Link](https://www.home-assistant.io/addons/rpc_shutdown/) | No | | |
| Wake on LAN | [Link](https://www.home-assistant.io/integrations/wake_on_lan/) | No | | |

### Sensors
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| Bayesian Sensors | [Link](https://www.home-assistant.io/integrations/bayesian/) | No | | |
| Cert Expiry | [Link](https://www.home-assistant.io/integrations/cert_expiry/) | No | | |
| Counter | [Link](https://www.home-assistant.io/integrations/counter/) | No | | |
| [DarkSky](https://darksky.net/dev) | [Link](https://www.home-assistant.io/integrations/weather.darksky/) | No | | |
| [Google Calendar](https://calendar.google.com/calendar/r) | [Link](https://www.home-assistant.io/integrations/calendar.google/) | No | | |
| History Stats | [Link](https://www.home-assistant.io/integrations/history_stats/) | No | | |
| Input Select | [Link](https://www.home-assistant.io/integrations/input_select/) | No | | |
| MQTT | [Link](https://www.home-assistant.io/docs/mqtt/) | Yes | [DIY Beacon](https://www.hackster.io/erictsai/lora-tooth-small-ble-sensors-over-wifi-lora-gateways-0aa109#toc-part--9--example--geolocation-beacon--amp--easy-button-14) | |
| MQTT | [Link](https://www.home-assistant.io/docs/mqtt/) | Yes | [Light Sensor](https://www.newark.com/advanced-photonix/norps-12/ldr-1mohm-250mw-norps-series/dp/07WX4951?CMP=AFC-SF-FC) | It's just a photoresistor connected to an MQTT gateway. |
| MQTT | [Link](https://www.home-assistant.io/docs/mqtt/) | Yes | [MiFlora Plant Sensor](https://gadget-freakz.com/product/xiaomi-mi-flora-plant-sensor/) | There is an integration for this, but the sensor is too far from my Pi, so in order to extend it's distance I grab the data and send it through MQTT - [Link](https://github.com/sidddy/flora) |
| Random Number | [Link](https://www.home-assistant.io/integrations/random/) | No | | |
| [SpeedTest](https://www.speedtest.net/) | [Link](https://www.home-assistant.io/integrations/speedtestdotnet/) | No | | |
| System Monitor | [Link](https://www.home-assistant.io/integrations/systemmonitor/) | No | | |
| Z-Wave | [Link](https://www.home-assistant.io/docs/z-wave/) | Yes | [Aeotec MultiSensor 6](https://aeotec.com/z-wave-sensor/) | |

### Switches
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [Amazon](https://www.amazon.com/) | None | Yes | [Amazon Smart Plug](https://www.amazon.com/Amazon-Smart-Plug-works-Alexa/dp/B01MZEEFNX) | This is not tied to Home Assistant, but it is connected to the power source for the Raspberry Pi.  This way, if push comes to shove I can remotely power cycle Home Assistant without needing access to it. |
| [TP-Link](https://www.tp-link.com/us/) | [Link](https://www.home-assistant.io/integrations/tplink/) | Yes | [HS100](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-hs100) | |
| [TP-Link](https://www.tp-link.com/us/) | [Link](https://www.home-assistant.io/integrations/tplink/) | Yes | [HS105](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-mini) | |
| [TP-Link](https://www.tp-link.com/us/) | [Link](https://www.home-assistant.io/integrations/tplink/) | Yes | [HS200](https://www.kasasmart.com/us/products/smart-switches/kasa-smart-wi-fi-light-switch-hs200) | |
| Z-Wave | [Link](https://www.home-assistant.io/docs/z-wave/) | Yes | [GE Smart Dimmer SKU#: 14294](https://byjasco.com/products/ge-z-wave-plus-wall-smart-dimmer) | |
| Z-Wave | [Link](https://www.home-assistant.io/docs/z-wave/) | Yes | [GE Smart Outlet SKU#: 14288](https://byjasco.com/products/ge-z-wave-plus-wall-tamper-resistant-smart-outlet) | |
| Z-Wave | [Link](https://www.home-assistant.io/docs/z-wave/) | Yes | [Jasco On/Off Swithc SKU#: 45709](https://www.z-wave.com/shop-z-wave-smart-home-products/smart-lighting-ge-jasco-jasco-white-in-wall-decora-style-on-off-z-wave-switch) | |
| Z-Wave | [Link](https://www.home-assistant.io/docs/z-wave/) | Yes | [Aeotec Nano Dimmer](https://aeotec.com/z-wave-light-dimmer-switch/) | A [bypass](https://aeotec.com/z-wave-low-voltage-dimmer/) was needed for some lights |

### Vacuum
| Component | Integration | Requires Purchase | Part | Comment |
|-----------|-------------|-------------------|------|---------|
| [Xiaomi Mi](https://www.mi.com/global) | [Link](https://www.home-assistant.io/integrations/vacuum.xiaomi_miio/) | Yes | [Xiaomi Mi Robot Vacuum](https://www.mi.com/roomrobot) | |

## Custom Integrations
These are the remaining items that I have running on my system.  Most are pulled from HACS, but there are one or two I have been working on myself.

* [HACS](https://github.com/hacs/integration)
* AppDaemon
  * Check Config
* Integrations
  * Alexa Media Player
  * Authenticated
  * Average Sensor
  * Breaking Changes
  * Clean Up Snapshots Service
  * Config Check
  * Favicon Changer
  * Illuminance
  * Lightpack - Requires Purchase 
  * Momentary Switch Component
  * Thingy:52 Sensor - Requires Purchase
  * WeatherAlerts
* Plugins
  * Compact Custom Header
  * Decluttering Card
  * Favicon Counter
  * Love Lock Card
  * Lovelace Toggle Lock Entity Row
  * Lovelace Xiaomi Vacuum Map Card
  * Mini Media Player
  * Simple Thermostat
  * Simple Weather Card
  * Swipe Card
  * Card Mod
  * Card Tools
  * Fold Entity Row
* Python Scripts
  * Power Usage Estimator
* Themes
  * Red Day Theme
  * Red Night Theme

# To Do List

## Things to Add
* Upstairs hallway 3-way light switch - No neutral wire available
* Downstairs hallway 3-way light switch - No neutral wire available
