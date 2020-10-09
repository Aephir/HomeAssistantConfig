# Motion sensors to control the basement entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):

        self.off_states = [
            'off',
            'unavailable',
            'unknown'
            ]

        # Motion sensors.
        self.listen_state(self.switch_on_off,"binary_sensor.presence_tv_room") # TV Room Motion Sensor

        # Illumination drops while motion sensor is "on" = light on.
        self.listen_state(self.switch_on_off,"sensor.lightlevel_tv_room")

        self.listen_state(self.input_boolean,"input_boolean.basement_lights_motion_control")

        self.listen_state(self.tv_off, 'media_player.ue55nu7475xxc')

    # Assess whether we are awake, based on state of entity. Find better proxy eventually.
    def are_we_awake(self, entity):
        if self.get_state(entity) == "on":
            return True

    # Return True/False for whether entity_id has state "on".
    def is_on(self, entity_id):
        return self.get_state(entity_id) == 'on'

    # Returns value of state as integer. Might need to remove the "float" is you get errors.
    def get_integer_state(self, entity_id):
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0

    # Motion sensor lights
    def switch_on_off(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state("binary_sensor.presence_tv_room") # TV Room Motion

        # # Add the commented, delete the rest once TV is set up downstairs
        # # ## Update "movie_night" with real entity_id once applicable. ##
        # # movie_night = self.is_on("media_player.tv_room_tv") # Are we using the TV lounge?
        #
        # if sensor_1_state == "on":
        #     if movie_night == "off":
        #         if self.get_integer_state("sensor.lightlevel_tv_room") < 15:
        #             self.turn_on("light.tv_room_lights",brightness=255,kelvin=2700)
        #             self.turn_on("light.basement_hallway",brightness=255,kelvin=2700)
        #
        # elif sensor_1_state == "off" and sensor_2_state == "off" and sensor_3_state == "off":
        #     self.turn_off("light.tv_room_lights")
        #     self.turn_off("light.basement_hallway")
        #
        # elif sensor_1_state == "off":
        #     self.turn_off("light.tv_room_lights")
        if self.get_state('media_player.ue55nu7475xxc') in self.off_states:
            if new == "on":
                self.turn_on("light.tv_room_lights",brightness=255,kelvin=2700)
            elif new == "off":
                self.turn_off("light.tv_room_lights")

    def input_boolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            self.switch_on_off(entity, attribute, old, new, kwargs)

    def tv_off(self, entity, attribute, old, new, kwargs):
        if new in self.off_states:
            self.switch_on_off(entity, attribute, old, new, kwargs)
