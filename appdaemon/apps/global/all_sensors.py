# List of all relevant sensors
# Use in another app by:
# app_config[you main app]['sensors']. For this app (all_sensors.py):
# app_config[all_sensors.py]['motionSensors']

# Ok there are 2 main ways to approach this, which I can suggest.
# Have the main app, in which in its config you have all your sensors, and give it a lower priority than 50; say 40. In the app, have it that when it starts up, it reads its args where you have the sensors, and it loads into the global_vars variable, so other apps can pick it up from there
# also ensure this app, is a dependent to other apps, so when you change the sensors, the others reload and get the new update
# another way to so it, is if you want to avoid loading into another variable, or avoid writing more code, all you can so is in the other apps, call app_config[you main app]['sensors']
# The others will always get the latest update
# Ensure in the main app config, they are put in there as a list or something

import appdaemon.plugins.hass.hassapi as hass

class GlobalSensors(hass.Hass):

    def initialize(self):
        return

    motionSensors = [
            "binary_sensor.presence_entrance", # Entrance
            "binary_sensor.presence_basement_entrance", # Basement entrance
            "binary_sensor.presence_top_floor_tv_room", # Basement stairway
            "binary_sensor.presence_tv_room", # TV room
            "binary_sensor.presence_conservatory", # Conservatory
            "binary_sensor.presence_top_floor_stairway", # Bathroom #1
            "binary_sensor.presence_bathroom_2", # Bathroom #2
            "binary_sensor.presence_top_floor_bathroom", # Upastairs bathroom
            "binary_sensor.presence_kitchen", # Kitchen
            "binary_sensor.conservatory_motion_sensor_aeotec", # Conservatory #2 (Aeotec)
            "binary_sensor.walk_in_closet_motion_sensor" # Walk-in closet
            ]

    illuminationSensors = [
        "sensor.lightlevel_entrance", # Entrance
        "sensor.illumination_158d000200d203", # Basement entrance
        "sensor.lightlevel_top_floor_tv_room", # Basement stairway
        "sensor.lightlevel_tv_room", # TV room
        "sensor.lightlevel_conservatory", # Conservatory
        "sensor.lightlevel_top_floor_stairway", # Bathroom #1
        "sensor.lightlevel_bathroom_2", # Bathroom #2
        "sensor.lightlevel_top_floor_bathroom", # Upastairs bathroom
        "sensor.lightlevel_kitchen", # Kitchen
        "sensor.aeotec_zw100_multisensor_6_luminance" # Walk-in closet
        # "sensor.illumination_7811dcb8d944" # Gateway illumination - remove
        ]

    doorSensors = [
        "binary_sensor.openclose_basement_entrance_door", # Basement door
        "binary_sensor.openclose_front_door", # Front door
        "binary_sensor.door_window_sensor_158d000234dc7b", # Conservatory door
        "binary_sensor.neo_coolcam_doorwindow_detector_sensor" # Shed sensor
        ]

    windowSensors = [
        "binary_sensor.openclose_bathroom_window", # Bathroom window
        "binary_sensor.openclose_bedroom_window_1" # Bedroom window #1
        ]

    doorbellRing = [
        "binary_sensor.skybell_front_door_button" # Doorbel button
        ]

    outdoorMotion = [
        "binary_sensor.skybell_front_door_motion" # Doorbell motion
        ]

    smokeDetector = [
        "binary_sensor.smoke_sensor_158d0001bc49bd" # Kitchen smoke detector
        ]

    plantTemperature = [
        "sensor.plant_sensor_1_temperature",
        "sensor.plant_sensor_2_temperature",
        "sensor.plant_sensor_3_temperature",
        "sensor.plant_sensor_4_temperature"
        ]

    mainFloorTemperatureSensors = [
        "sensor.temperature_bathroom", # Bathroom
        "sensor.aeotec_zw100_multisensor_6_temperature_2", # Conservatory
        "sensor.fibaro_system_fgt001_heat_controller_temperature", # Bathrooom Fibaro thermostat
        "sensor.temperature_kitchen" # Kitchen
        ]

    topFloorTemperatureSensors = [
        "sensor.temperature_top_floor_tv_room" # Top floor living room
        ]

    basementTemperatureSensors = [
        "sensor.aeotec_zw100_multisensor_6_temperature", # Walk-in closet
        "sensor.temperature_washing_room", # Washing room
        "sensor.temperature_wine_cellar", # Wine cellar
        ]

    outdoorTemperatureSensors = [
        "sensor.temperature_washing_room" # Shed
        ]

    mainFloorHumiditySensors = [
        "sensor.humidity_bathroom", # Bathroom
        "sensor.aeotec_zw100_multisensor_6_relative_humidity_2", # Conservatory
        "sensor.humidity_kitchen" # Kitchen
        ]

    topFloorHumiditySensors = [
        "sensor.humidity_top_floor_tv_room" # Top floor living room
        ]

    basementHumiditySensors = [
        "sensor.aeotec_zw100_multisensor_6_relative_humidity", # Walk-in closet
        "sensor.humidity_washing_room", # Washing room
        "sensor.humidity_wine_cellar" # Wine cellar
        ]

    outdoorHumiditySensors = [
        "sensor.humidity_washing_room" # Shed
        ]

    pressureSensors = [
        "sensor.pressure_bathroom", # Bathroom
        "sensor.pressure_wine_cellar", # Washing room
        "sensor.pressure_158d000245b4a2", # Wine cellar
        "sensor.pressure_washing_room" # Shed
        ]


    # batterySensors
    # plantSensors # conductivity, temperature, etc.
