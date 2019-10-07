# Home Assistant
My third version of homeassistant. This time on a Fujitsu Esprimo q520 (i3 version) with Ubuntu Server LTS 18.04 running (almost) everything in Docker. This guide will be updated to reflect this over the next couple of months (while I'm moving to a new house, and adjusting everything).

I drew quite a bit of inspiration from [COOSTAN](https://github.com/CCOSTAN/Home-AssistantConfig), [dale3h](https://github.com/dale3h/homeassistant-config), [arsaboo](https://github.com/arsaboo/homeassistant-config), as well as [a few others](https://www.home-assistant.io/cookbook/), so look there if any of this is interesting. If I give my endorsement to, or give negative comments about anything, they are merely things I personally like/dislike. I have no affiliation to any of them or their potential competitors, and my positive or negative comments are based exclusively on my personal preference.

____
EVERYTHING IS A WORK IN PROGRESS. LOT'S OF STUFF IS COMMENTED OUT WHILE I TRY DIFFERENT THINGS. THAT'S NOT LIKELY TO CHANGE ANY TIME SOON :-)

Some additional scripts, files that contain sensitive information (but where I want to save a "template"), etc. can be found in my [additional files](https://github.com/Aephir/Home_Assistant-Accessory-files) repo.

**Hardware**
* [Fujitsu Esprimo q520](https://sp.ts.fujitsu.com/dmsp/publications/public/ds-esprimo-q520.pdf) running almost everything described below.
* [Raspberry Pi 3B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) running hass.io to connect to plant sensors (no bluetooth on Esprimo, plus I want this to be close to the greenhouse once that is set up. I'm not sure the main PC would even be within bluetooth range).
* [Aeotec Z-Stick Gen5](https://aeotec.com/z-wave-usb-stick) z-wave USB controller.
* [ConBee II USB stick](https://www.phoscon.de/en/conbee2) ZigBee USB controller.
* ~~[DHT22](https://www.adafruit.com/product/385) for indoor temperature and moisture sensor.~~
* [Philips Hue Lights](https://www2.meethue.com/en-us), a mix of various colored and white bulbs, and a single lighstrip running on the old bridge (v1).
* [IKEA TRÅDFRI](https://www.ikea.com/us/en/catalog/categories/departments/lighting/36812/) bulbs, connected to the hue bridge.
* [Philips Hue Dimmer Switches](https://www2.meethue.com/en-us/p/hue-dimmer-switch/046677458140), hacked with the help of [this guide](https://www.hackster.io/robin-cole/hijack-a-hue-remote-to-control-anything-with-home-assistant-5239a4) and the corresponding forum thread.
* [Belkin WeMo Insight Switches](http://www.belkin.com/us/p/P-F7C029/), two insight switches, though these are "legacy" in my setup, future smart switches will be z-wave. When we bought our house, part of the deal was that we "inherited" a fountain in the garden, so of course I've set this up for control through Home Assistant with one of the old WeMos :-)
* [Fibaro Wall Plug](https://www.fibaro.com/en/products/wall-plug/) z-wave power outlet switch. Master switch for the media center (TV, Stereo, PS4, etc.). I have had a very good experience with Fibaro, and plan to include more plugs and/or other Fibaro devices.
* [NeoCoolCam](http://www.szneo.com/en/products/index.php?id=41) to cut power to my desktop PC (it'll find a better use in a few months after we move)
* [Raspberry Pi 3B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) running [Kodi](https://kodi.tv/) (switch a bit between raspbian + kodi and [LibreELEC](https://libreelec.tv/), connected to TV (CEC commands can be sent to this Pi via SSH to control TV). This has the [HiFiBerry DAC+ Pro](https://www.hifiberry.com/shop/boards/hifiberry-dac-pro/) for high fidelity audio output.
* [Raspberry Pi 2B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) Running [Mopidy](https://www.mopidy.com/). It is set up via MPD, though mostly controlled independently of Home Assistant, though (using primarily the very nice [Iris](https://github.com/jaedb/Iris) interface by jaedb). Connected to proper effect amplifier (NAD c275bee). This has the [Allo BOSS Maser DAC](https://www.modmypi.com/raspberry-pi/audio-dacampdigi/dacs-digital-to-analogue-coverters-1044/allo-boss-raspberry-pi-master-dac/?secumt=I3RhYi1yZXZpZXc=#review-title) for high fidelity audio output.
* [SONOS Play 5](https://www.sonos.com/en/shop/play5.html) for low fidelity playback and TTS from home assistant.
* [Google Home Mini](https://store.google.com/?srp=/product/google_home_mini) mostly to use as microphone; I have home assistant set up with google assistant via home assistant cloud.
* [Chromecasts](https://store.google.com/product/chromecast). Easier/better control of certain TVs
* [Chromecast Audio](https://store.google.com/product/chromecast_audio). Easier/better control and linking of various speakers and hifi systems.
* [iKettle](https://smarter.am/support-ikettle-1-0/). Yeah, even I will admit this one is a bit overkill, unless you use a kettle at least daily. Otherwise (1) the water goes stale before you use it or (2) you have to go and fill/change the water, and then you might as well press the button manually while you're there. Still a nice kettle, even without the connectivity, but probably wouldn't buy a connected kettle again.
* [Smart TV](http://www.samsung.com/dk/support/model/UE46ES8005UXXE) (though integration is not that useful at the moment, the old fashioned remote or smartphone app is used much more).
* [Xiaomi Gateway](https://xiaomi-mi.com/mi-smart-home/xiaomi-mi-gateway-2/)
* [Xiaomi Motion Sensor](https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-occupancy-sensor/), that also measures illuminance.
* [Xiaomi Temperature/Humidity/Barometric Pressure Sensor](https://xiaomi-mi.com/sockets-and-sensors/aqara-temperature-and-humidity-sensor/), set up in bathroom, wine cellar, shed etc.
* [Xiaomi Door/Window Sensor](https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-door-window-sensors/).
* [Xiaomi Smart Home Wireless Switch](https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-wireless-switch/), I'm, loving this one! Super simple, just one button next to my bed, but automated to do what I need (turn on coffee machine if it's morning, turn off lights if it's night, keep on a night light upstairs if the kids are home, etc.)
* [Neo CoolCam Door/Window Sensor](http://www.szneo.com/en/products/index.php?id=42) a z-wave door/window sensor.
* [Huahuacaocao Flower Care Smart Monitor](https://xiaomi-mi.com/sockets-and-sensors/xiaomi-huahuacaocao-flower-care-smart-monitor/) for monitoring my plants. I'm thinking they'll come in handy when I get a greenhouse, where I can automate windows/watering.
* [Xiaomi Honeywell Smoke Detector](https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mijia-honeywell-smoke-detector-white/).
* [Skybell HD Trim Plus](http://www.skybell.com/product/skybell-video-doorbell-trim-plus/). It works, but you can't really directly use home assistant to react when someone rings; there's a 10 - 40 second delay. I use a tablet in the basement with Tasker to send a POST via RESTask to home assistant.
* [Aeotec MultiSensor 6](https://aeotec.com/z-wave-sensor). Using as a sensor (motion, temperature, etc.), but cabled, so also using as z-wave repeaters.
* [Fibaro Heat Controller](https://www.fibaro.com/en/products/the-heat-controller/), one so far. Having some issues with proper control and updating information in HASS. Ongoing...

**Software:** 
* [Ubuntu Server LTE 18.04](https://downloads.raspberrypi.org/raspbian_lite_latest) as the OS.
* [mlocate](https://wiki.debian.org/sSMTP) for finding stuff.
* [Samba](https://www.samba.org/samba/what_is_samba.html) for easy modification of config files.
* [SSHFS](https://en.wikipedia.org/wiki/SSHFS), Iv'e started to use this instead of Samba. You can mount drives via SSHFS, and it is seemingly somewhat more secure than Samba. I access from MacOS, so I'm using [Fuse and SSHFS for mac](https://osxfuse.github.io/).
* [Docker](https://www.docker.com/) for as much as possible.
* [Docker Compose](https://docs.docker.com/compose/) for a single file containing (almost) all info for all my docker containers
* [Unattended upgrades](https://help.ubuntu.com/community/AutomaticSecurityUpdates) to keep up to date with security updates.
* [hass.io](https://www.home-assistant.io/hassio/) running on RPi3B, and using the [Bluetooth BCM43xx](https://www.home-assistant.io/addons/bluetooth_bcm43xx/), [samba](https://www.home-assistant.io/addons/samba/), and [SSH Server](https://www.home-assistant.io/addons/ssh/) add-ons.


**Docker Containers:**
OBS! Some are not fully configured yet.
* [DuckDNS](http://www.duckdns.org/) [docker container](https://hub.docker.com/r/linuxserver/duckdns/) for external access to Home Assistant.
* [Let's Encrypt](https://letsencrypt.org/) [docker container](https://hub.docker.com/r/linuxserver/letsencrypt/) for certificates.
* [NGINX](https://www.nginx.com/) [docker container](https://hub.docker.com/r/linuxserver/letsencrypt/) is included in the "Let's Encrypt" image. Used to securely expose only the services I choose (e.g.  Home Assistant) via SSL to the big bad web. Everything else is run locally, and not accessible from the outside.
* [Home Assistant](https://www.home-assistant.io/) [docker container](https://hub.docker.com/r/homeassistant/home-assistant/) for all my home control and automation needs.
* [Mosquitto](https://mosquitto.org/2013/01/mosquitto-debian-repository/) [docker container](https://hub.docker.com/_/eclipse-mosquitto/) for for reporting of plant sensor states from a hass.io on a RPi3B, and future applications.
* [deCONZ](https://www.dresden-elektronik.de/funktechnik/products/software/pc/deconz/) [docker container](https://hub.docker.com/r/marthoc/deconz) for controlling all ZigBee devices.
* [MariaDB](https://mariadb.org/) [docker container](https://hub.docker.com/_/mariadb/)
* [Syncthing](https://syncthing.net/) [docker container](https://hub.docker.com/r/linuxserver/syncthing/)
* [AppDaemon](https://appdaemon.readthedocs.io/en/latest/) [docker container](https://hub.docker.com/r/acockburn/appdaemon/)
* [HA Dockermon](https://github.com/philhawthorne/ha-dockermon) [docker container](https://hub.docker.com/r/philhawthorne/ha-dockermon/)
* [Portainer](https://portainer.io/) [docker container](https://hub.docker.com/r/portainer/portainer/)
* [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/) [docker container](https://hub.docker.com/_/influxdb/)
* [Grafana](https://grafana.com/) [docker container](https://hub.docker.com/r/grafana/grafana/)
* [Node-RED](https://nodered.org/) [docker container](https://hub.docker.com/r/nodered/node-red-docker/)


**Useful scripts set up with crontab**
* [rsync](https://packages.debian.org/stretch/rsync) script run in crontab for keeping a partial backup on SD card. Not entire image, it's much faster, and takes up less space.
* [Life360](https://www.life360.com/) for device tracking. I've found that owntracks just doesn't cut it (too slow/irregular update of location, so can't use it to automate based on entering/exiting areas), and so far Life360 is the best device tracker I've found. I am using the version provided by [pnbruckner](https://community.home-assistant.io/t/life360-device-tracker-platform/52406).
* script to send email with new IP when IP changes. This is mostly for SSH access from outside my home network.


**Notable Home Assistant components**
* [Floorplan](https://github.com/pkozul/ha-floorplan), a great project by pkozul to visualize your home with interactive gadgets.

![Screenshot Floorplan](https://github.com/Aephir/Images/blob/master/floorplan_20181202.png)
_Floorplan - Circles with temperature/humidity states can be clicked to toggle all lights in that room. Individual bulbs (black or yellow circles when off/on) can be toggled. Info about us in the top left side (location and battery status), toggles/scripts/scenes on the right side. The outer doors have door sensors, if closed they are "invisible", if opened, they show a big fat red quarter-circle so you're not in doubt. Some stuff, such as phone battery level indicators and temperatures, changes color based on values. Alarm system status is shown at the bottom, and the greenhouse (just plants for now, greenhouse will likely not come until next year) is the blue rectangle at the top with plant data. In time, I want the buttons showing "Upstairs", "Ground Floor", and "Top Floor" to toggle "pop-ups" zooming in on that floor for more in depth info and control. If I find this useful for control, that is. I actually like it more because it's cool, I haven't used it since we moved (it was easier to fit a small apartment in a scale that was usable)._

**Frontend**
Frontend using lovelace, so it is currently being rearranged and updated as I become more comfortable with lovelace, and as lovelace evolves.


**Custom cards and components**
Currently, I use the following [integrations and custom cards](https://github.com/ciotlosm/custom-lovelace):
* [Monster Card](https://github.com/ciotlosm/custom-lovelace/tree/master/monster-card), mostly for the entity_filter. It's very useful when you add e.g. a new light, and don't want to dig through to find the entity_id. I have a card with all lights that are 'on' and a card with all lights that are 'off'. Easy to find and change name/entity_id.
* [Gauge Card](https://github.com/ciotlosm/custom-lovelace/tree/master/gauge-card). Is it necessary? No. Does it look cool? Yes! I use it for computer stats.
* [Slider](https://github.com/thomasloven/lovelace-slider-entity-row) because I loved this feature of * [Custom UI](https://github.com/andrey-git/home-assistant-custom-ui).
* [Toggle Lock](https://github.com/thomasloven/lovelace-toggle-lock-entity-row) because I need to make something so the kids can't control the expresso machine and the lights in our bedroom while we wait for more features of the user system.
* [Custom Updater](https://github.com/custom-components/custom_updater). Because I want to use the custom tracker.
* [Tracker Card](https://github.com/custom-cards/tracker-card). Do I want to manually keep track of versions of the custom cards and components? No way.
* [Life360](https://github.com/pnbruckner/homeassistant-config/blob/master/custom_components/device_tracker/life360.py). This is one of the better device trackers out there. I combine it with a few others in an appdaemon script for a slightly better tracker. But if I could only choose one, this would be it.

**Notable automations**
* Integrate presence sensing for each family member into "anyone home" input_boolean. Used to automate various things.
* Turn on lights if anyone arrives home later than 1 hour before sunset.
* Turn on living room lights 1 hour before sunset if someone home (plan to either implement light sensors or sun angle instead in future).
* Guest mode - An input_boolean toggle that disables all the general presence-based automations (so the lights don't go out once you leave, if a guest is staying).
* Motion sensors everywhere, to control light. At night time (unless certain other lights are on, or the TV is on, etc.), the light in the bathroom will turn on at 10% and be red to avoid waking up too much.
* Automations for my bedside button. Depending on various factors (time of day, workday or day off, kids at home or not, etc.) it will do various things. Usually, it starts up the espresso machine if I press it in the morning, and does various things with the light and/or turning off various appliances if I press it in the evening/night.


**Notable Scripts**
* Python script to use hue dimmer remotes. I might go to pure automations, since I can't get the python script to use both "click" and "long-press".
* turn off lights, espresso machine, send shutdown command through SSH to two Raspberry Pis (KODI and Mopidy) before cutting the master power to those 15 seconds later. Used in various automations (such as when no one is home, when we go to bed, etc.)
* Appdaemon scripts to send stuff to Tasker. I have a bunch of things here, take a look at [this repo](https://github.com/Aephir/Home_Assistant-Accessory-files/tree/master/appdaemon_scripts) for some examples (with redacted info, many of them have my Joaoapps Join key in the url). Also, look in this repo for various AppDaemon scripts (the ones without redacted info).

![KWGT widget](https://github.com/Aephir/Images/blob/master/Screen%20Shot%202018-11-02%20at%2012.13.20%20.png)
_The first Kustom (KWGT) widget. Everything happens through Home Assistant. Each light changes on/off color regardless of where it is switched from (HASS sends state changes to Tasker). Espresso and Fountain are just toggle switches, the middle arrow buttons will (hopefully) become brightness up/down on last light turned on. The text i the botton currently just tells me which was the last door that was opened._


**Notable Other**
* I (finally) started using [Tasker](http://tasker.dinglisch.net/) again. The nudge I needed was my doorbell, that has a huge delay if using purely home assistant. I use it with the [RESTask](https://play.google.com/store/apps/details?id=com.freehaha.restask&hl=en) plugin, in able to use the new long-lived access tokens instead of api password.
* Kustom (KWGT) to make widgets on my phone that can control anything from Home Assistant (and receive info from Home Assistant)


**Planned future software:**
* Samba in Docker?
* Or perhaps [SSHFS](https://wiki.archlinux.org/index.php/SSHFS) mounting for more secure access?
* Combine all my motion sensors into python scripts; avoid having 20 automations that could be solved by one or two python scripts. Oh, and learn Python while I'm at it :-)


**Planned future hardware**
A bunch of this is stuff I have lying around, but haven't figured out how to use yet. Other things are on the wishlist
* Arduino (several, for a few different purposes).
* NRF24L01 RF transceiver (several, for a few different purposes).
* [WyzeCam](https://www.wyzecam.com/) - currently not possible (afaik) to integrate, but I contacted them, and they said they would look into it. So let's see.
* HCSR501 PIR sensors
* [Matrix Voice](https://www.indiegogo.com/projects/matrix-voice-open-source-voice-platform-for-all) backed on IndieGoGo, should arrive in early 2018. Will then set up either a [snips](https://snips.ai/) or [google assistant](https://assistant.google.com/)/[Alexa](https://www.amazon.com/Amazon-Echo-And-Alexa-Devices/b?ie=UTF8&node=9818047011). UPDATE. I have used it, and can successfully set up Google Assistant, but I'm having issues setting up snips (I tried in Docker, maybe I'll give it a go without Docker). Will try again later.
* [Xiaomi Light Switch](https://xiaomi-mi.com/sockets-and-sensors/xiaomi-aqara-smart-light-control-set/) Not yet implemented, for new home.
* [Sonoff switch with power consumption measurement](https://www.itead.cc/sonoff-pow.html) for my shed/workshop once I move.
* [Sonoff Wall Touch Switch](https://www.itead.cc/sonoff-t1.html) for the new house. I have a few different ones I want to test.
* [Fibaro Radiator Thermostat](https://www.fibaro.com/en/products/the-heat-controller/). They seem like the best ones for integrating with Home Assistant. Not sure if I should get the Z-wave or bluetooth version, though (bluetooth version is advertized as Apple Homekit version, but maybe bluetooth is better? Probably not though, but I need to look into this).


**Planned future misc.**
* Integrate various  additional stuff with Tasker. Have Tasker send info to home assistant, then have home assistant do the work.
