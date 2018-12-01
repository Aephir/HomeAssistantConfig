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
            "binary_sensor.motion_sensor_158d00023e3742", # Entrance
            "binary_sensor.motion_sensor_158d000200d203", # Basement entrance
            "binary_sensor.motion_sensor_158d000236a0f3", # Basement stairway
            "binary_sensor.motion_sensor_158d000236a116", # TV room
            "binary_sensor.motion_sensor_158d000200d285", # Conservatory
            "binary_sensor.motion_sensor_158d000200e0c5", # Bathroom #1
            "binary_sensor.motion_sensor_158d000236a22f", # Bathroom #2
            "binary_sensor.motion_sensor_158d000236a0d0", # Upastairs bathroom
            "binary_sensor.motion_sensor_158d0001e0a8e1" # Kitchen
            ]



    illuminationSensors = [
        "sensor.illumination_158d00023e3742", # Entrance
        "sensor.illumination_158d000200d203", # Basement entrance
        "sensor.illumination_158d000236a0f3", # Basement stairway
        "sensor.illumination_158d000236a116", # TV room
        "sensor.illumination_158d000200d285", # Conservatory
        "sensor.illumination_158d000200e0c5", # Bathroom #1
        "sensor.illumination_158d000236a22f", # Bathroom #2
        "sensor.illumination_158d000236a0d0", # Upastairs bathroom
        "sensor.illumination_158d0001e0a8e1" # Kitchen
        # "sensor.illumination_7811dcb8d944" # Gateway illumination - remove
        ]

    doorWindowSensors = [
        "binary_sensor.door_window_sensor_158d0002286a78", # Bathroom window
        "binary_sensor.door_window_sensor_158d00022b3b66", # Basement door
        "binary_sensor.door_window_sensor_158d00022d0917", # Front door
        "binary_sensor.door_window_sensor_158d000234dc7b", # Conservatory door
        "binary_sensor.neo_coolcam_doorwindow_detector_sensor" # Shed sensor
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

    ]

    humiditySensors = [
    "sensor.humidity_158d00022c66ff", # Bathroom
    "sensor.humidity_158d0002437897", # Washing room
    "sensor.humidity_158d000245b4a2", # Wine cellar
    "sensor.humidity_158d000243778b" # Shed
    ]

    pressureSensors = [
    "sensor.pressure_158d00022c66ff", # Bathroom
    "sensor.pressure_158d0002437897", # Washing room
    "sensor.pressure_158d000245b4a2", # Wine cellar
    "sensor.pressure_158d000243778b" # Shed
    ]

    temperatureSensors = [
    "sensor.temperature_158d00022c66ff", # Bathroom
    "sensor.temperature_158d0002437897", # Washing room
    "sensor.temperature_158d000245b4a2", # Wine cellar
    "sensor.temperature_158d000243778b" # Shed
    ]

    # batterySensors
    # plantSensors # conductivity, temperature, etc.
