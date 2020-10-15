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

        self.listen_state(self.switch_on_off,"input_boolean.basement_lights_motion_control", new='on')

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

        if self.get_state('media_player.ue55nu7475xxc') in self.off_states:
            if sensor_1_state == "on":
                self.turn_on("light.tv_room_lights",brightness=255,kelvin=2700)
            elif sensor_1_state == "off":
                self.turn_off("light.tv_room_lights")
                

    def tv_off(self, entity, attribute, old, new, kwargs):
        if new in self.off_states:
            self.switch_on_off(entity, attribute, old, new, kwargs)
