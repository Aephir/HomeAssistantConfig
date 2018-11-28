# List of all sensors

import appdaemon.plugins.hass.hassapi as hass

class SensorIds(hass.Hass):

    self.motionSensors = [
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

    self.illuminationSensors = [
        "sensor.illumination_158d00023e3742", # Entrance
        "sensor.illumination_158d000200d203", # Basement entrance
        "sensor.illumination_158d000236a0f3", # Basement stairway
        "sensor.illumination_158d000236a116", # TV room
        "sensor.illumination_158d000200d285", # Conservatory
        "sensor.illumination_158d000200e0c5", # Bathroom #1
        "sensor.illumination_158d000236a22f", # Bathroom #2
        "sensor.illumination_158d000236a0d0", # Upastairs bathroom
        "sensor.illumination_158d0001e0a8e1" # Kitchen
        # "sensor.illumination_7811dcb8d944" # Gateway illumination - remoce
        ]

    self.doorWindowSensors = [
        "binary_sensor.door_window_sensor_158d0002286a78", # Bathroom window
        "binary_sensor.door_window_sensor_158d00022b3b66", # Basement door
        "binary_sensor.door_window_sensor_158d00022d0917", # Front door
        "binary_sensor.door_window_sensor_158d000234dc7b", # Conservatory door
        "binary_sensor.neo_coolcam_doorwindow_detector_sensor", # Shed sensor
        ]

    self.doorbellRing = [
        "binary_sensor.skybell_front_door_button" # Doorbel button
        ]

    self.outdoorMotion = [
        "binary_sensor.skybell_front_door_motion" # Doorbell motion
        ]

    self.smokeDetector = [
        "binary_sensor.smoke_sensor_158d0001bc49bd" # Kitchen smoke detector
        ]

    self.plantTemperature = [

    ]

    self.humiditySensors = [
    "sensor.humidity_158d00022c66ff", # Bathroom
    "sensor.humidity_158d0002437897", # Washing room
    "sensor.humidity_158d000245b4a2", # Wine cellar
    "sensor.humidity_158d000243778b" # Shed
    ]

    self.pressureSensors = [
    "sensor.pressure_158d00022c66ff", # Bathroom
    "sensor.pressure_158d0002437897", # Washing room
    "sensor.pressure_158d000245b4a2", # Wine cellar
    "sensor.pressure_158d000243778b" # Shed
    ]

    self.temperatureSensors = [
    "sensor.temperature_158d00022c66ff", # Bathroom
    "sensor.temperature_158d0002437897", # Washing room
    "sensor.temperature_158d000245b4a2", # Wine cellar
    "sensor.temperature_158d000243778b" # Shed
    ]

    # batterySensors
    # plantSensors # conductivity, temperature, etc.
