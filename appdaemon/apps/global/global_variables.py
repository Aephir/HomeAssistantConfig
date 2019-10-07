# Global variables
# Use by importing in other apps
# import global_variables

motionSensors = [
    "binary_sensor.presence_entrance", # Entrance
    "binary_sensor.presence_basement_entrance", # Basement entrance
    "binary_sensor.presence_top_floor_tv_room", # Basement stairway
    "binary_sensor.presence_tv_room", # TV room
    "binary_sensor.presence_conservatory", # Conservatory
    "binary_sensor.presence_top_floor_stairway", # Bathroom #1
    "binary_sensor.presence_bathroom_2", # Bathroom #2
    "binary_sensor.presence_top_floor_bathroom", # Upastairs bathroom
    "binary_sensor.presence_kitchen" # Kitchen
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
    "sensor.lightlevel_kitchen" # Kitchen
    # "sensor.illumination_7811dcb8d944" # Gateway illumination - remove
    ]

doorWindowSensors = [
    "binary_sensor.openclose_bathroom_window", # Bathroom window
    "binary_sensor.openclose_basement_entrance_door", # Basement door
    "binary_sensor.openclose_front_door", # Front door
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
    ''
    ]

humiditySensors = [
"sensor.humidity_bathroom", # Bathroom
"sensor.humidity_washing_room", # Washing room
"sensor.humidity_wine_cellar", # Wine cellar
"sensor.humidity_washing_room" # Shed
]

pressureSensors = [
"sensor.pressure_bathroom", # Bathroom
"sensor.pressure_wine_cellar", # Washing room
"sensor.pressure_158d000245b4a2", # Wine cellar
"sensor.pressure_washing_room" # Shed
]

temperatureSensors = [
"sensor.temperature_bathroom", # Bathroom
"sensor.temperature_washing_room", # Washing room
"sensor.temperature_wine_cellar", # Wine cellar
"sensor.temperature_washing_room" # Shed
]
