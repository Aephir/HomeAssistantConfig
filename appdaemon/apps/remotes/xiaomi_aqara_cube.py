"""
Xiaomi cube remote
"""

import appdaemon.plugins.hass.hassapi as hass
# import datetime

class Remote(hass.Hass):

# action_type, action_value (rotate)
# last_action:
        # flip90, flip180, move, tap_twice, shake_air, swing, alert, free_fall, rotate (degrees at action_value)
# last_action (that I can actually get to work reliably):
        # rotate, flip90, flip180, move, shake_air, free_fall
# last_action (that I have seen, but can't reproduce reliably):
        # alert


    def initialize(self):

        # List of light groups that can be "active". If active, this is what is dimmed upon rotation.
        # self.light_list = [
        #     'light.kitchen_spots',
        #     'light.dining_room_lights',
        #     'light.conservatory_lights'
        #     ]

        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.button_state,"binary_sensor.cube_158d00028f7196")


    def button_state(self, entity, attribute, old, new, kwargs):
        # "new" will be "flip90", "flip180", "move", "tap_twice", "shake_air", "swing", "alert", "free_fall", and "rotate".
        # "action_value" will be available if "new" == "rotate". If so, "action_type" will be degrees of rotation.

        top_floor_lights = [
            'light.top_floor_hallway',
            'light.top_floor_tv_area'
            ]

        for light in top_floor_lights:
            self.toggle(light)
        #
        # raw_value = self.get_state("binary_sensor.cube_158d00028f7196", attribute = "value")
        # action = self.get_state("binary_sensor.cube_158d00028f7196", data = "action_value")
        # self.log(raw_value)
        # self.log(action)
        #
        # last_action = self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action")
        #
        # if last_action == move:
        # elif last_action == rotate:
        # # elif last_action == flip90:
        # #     # Snooze alarm if within 30 minutes after alarm time is set.
        # # elif last_action == flip180:
        # #     # Cancel alarm if within 30 minutes after alarm time is set.
        # elif last_action == shake_air:
        #     self.goodNight()


    # def goodNight(self, entity, attribute, old, new, kwargs):
