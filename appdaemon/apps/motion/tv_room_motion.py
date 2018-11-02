# Motion sensors to control the basement entrance lights

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):
        # Motion sensors.
        self.listen_state(self.switchonoff,"binary_sensor.motion_sensor_158d000236a116") # TV Room Motion Sensor
        self.listen_state(self.switchonoff,"binary_sensor.motion_sensor_158d000236a0f3") # Basement Stairway Motion Sensor
        # Illumination drops while motion sensor is "on" = light on.
        self.listen_state(self.switchonoff,"sensor.illumination_158d000200d203")

    # Assess whether we are awake, based on state of entity. Find better proxy eventually.
    def areWeAwake(self, entity):
        if self.get_state(entity) == "on":
            return True

    # Return True/False for whether entity_id has state "on".
    def isOn(self, entity_id):
        return self.get_state(entity_id) == 'on'

    # Returns value of state as integer. Might need to remove the "float" is you get errors.
    def getIntegerState(self, entity_id):
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0

# Motion sensor lights
    def switchonoff(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state("binary_sensor.motion_sensor_158d000236a116") # TV Room Motion
        sensor_2_state = self.get_state("binary_sensor.motion_sensor_158d000236a0f3") # Basement Stairway Motion
        sensor_3_state = self.get_state("binary_sensor.motion_sensor_158d000200d203") # Basement Entrance Motion

        # # Add the commented, delete the rest once TV is set up downstairs
        # # ## Update "movie_night" with real entity_id once applicable. ##
        # # movie_night = self.isOn("media_player.tv_room_tv") # Are we using the TV lounge?
        #
        # if sensor_1_state == "on":
        #     if movie_night == "off":
        #         if self.getIntegerState("sensor.illumination_158d000236a116") < 15:
        #             self.turn_on("light.tv_room_lights",brightness=255,kelvin=2700)
        #             self.turn_on("light.basement_hallway",brightness=255,kelvin=2700)
        #
        # elif sensor_1_state == "off" and sensor_2_state == "off" and sensor_3_state == "off":
        #     self.turn_off("light.tv_room_lights")
        #     self.turn_off("light.basement_hallway")
        #
        # elif sensor_1_state == "off":
        #     self.turn_off("light.tv_room_lights")

        if sensor_1_state == "on":
            self.turn_on("light.tv_room_lights",brightness=255,kelvin=2700)
            self.turn_on("light.basement_hallway",brightness=255,kelvin=2700)

        elif sensor_1_state == "off" and sensor_2_state == "off" and sensor_3_state == "off":
            self.turn_off("light.tv_room_lights")
            self.turn_off("light.basement_hallway")

        elif sensor_1_state == "off":
            self.turn_off("light.tv_room_lights")

# # Get states of motion sensors
# entrance_motion_state = self.get_state("binary_sensor.motion_sensor_158d00023e3742")
# basement_entrance_motion_state = self.get_state("binary_sensor.motion_sensor_158d000200d203")
# basement_stairway_motion_state = self.get_state("binary_sensor.motion_sensor_158d000236a0f3")
# tv_room_motion_state = self.get_state("binary_sensor.motion_sensor_158d000236a116")
# conservatory_motion_state = self.get_state("binary_sensor.motion_sensor_158d000200d285")
# bathroom_1_motion_state = self.get_state("binary_sensor.motion_sensor_158d000200e0c5")
# bathroom_2_motion_state = self.get_state("binary_sensor.motion_sensor_158d000236a22f")
# bathroom_upstairs_motion_state = self.get_state("binary_sensor.motion_sensor_158d000236a0d0")
