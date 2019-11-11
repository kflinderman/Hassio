# Home Assistant Configuration
This is my primary [Home Assistant](https://home-assistant.io/) configuration, This instance is running 0.101.3 on a Raspberry Pi 3B+ with the [HassOS](https://github.com/home-assistant/hassos) operating system runn HassIO.  It was installed [following this guide](https://www.home-assistant.io/hassio/installation/).

# Structure
* AppDaemon
* DuckDNS
* Emulated Hue
* Graphana
* InfuxDB
* Let's Encrypt
* MariaDB
* Mosquitto
* SSH & Web Terminal
* Z-Wave

# Integrations, Devices, and Services
Here is a list of all of the devices and services that I use.  I will link to each integration.  I will also indicated which ones require purchasing an item, I'll do this because I'm always surprised about what is available to make your home smart with what is readily available for free.  I have not included everything here, because some are custom integrations which I will discuss separately.

* Cameras
  * Amcrest
    * Outside One - Requires Purchase
    * Inside One - Requires Purchase - 
  * Skybell - Requires Purchase
* Device Trackers
  * GPSLogger
  * Home Assistant Bluetooth
  * Home Assistant IOS App
  * Netgear Router - Requires Purchase
* HVAC
  * Ecobee - Requires Purchase
* Lights
  * Phillips Hue - Requires Purchase
* Media Players
  * Google Play Music Desktop Player
  * LG Netcast - Requires Purchase
  * Yamaha AVR - Requires Purchase
* Notifications
  * Home Assistant IOS App
  * Pushbullet
* Other
  * IFTTT
* PC Control
  * RPC Shutdown
  * Wake on LAN
* Sensors
  * Speed Test
  * Dark Sky
  * Google Calendar
  * Counter
  * Input Select
  * MQTT
    * Dog Location Tracker - Requires Purchase
    * Light Sensor - Requires Purchase
    * Xiaomi Mi Plant Sensor - Requires Purchase
  * Bayesian Sensors
  * System Monitor
  * Random Number
  * Cert Expiry
  * History Stats
* Switches
  * TP-Link - Requires Purchase
  * Z-Wave - Requires Purchase
* Vacuum
  * Xiaomi Mi Vacuum - Requires Purchase

# Custom Integrations
These are the remaining items that I have runnin on my system.  Most are pulled from HACS, but there are one or two I have been working on myself.

* HACS
* AppDaemon
  * Check Config
* Integrations
  * Alexa Media Player - Requires Purchase
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
