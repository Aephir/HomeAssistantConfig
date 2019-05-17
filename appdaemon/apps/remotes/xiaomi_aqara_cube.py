"""
Xiaomi cube remote
"""

import appdaemon.plugins.hass.hassapi as hass

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
        self.light_list = [
            'light.kitchen_spots',
            'light.dining_room_lights',
            'light.conservatory_lights'
            ]

        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.ButtonState,"binary_sensor.cube_158d00028f7196")


    def ButtonState(self, entity, attribute, old, new, kwargs):
        # "new" will be "flip90", "flip180", "move", "tap_twice", "shake_air", "swing", "alert", "free_fall", and "rotate".
        # "action_value" will be available if "new" == "rotate". If so, "action_type" will be degrees of rotation.

        light_id = ''

        # Tap twice to cycle "active lights".
        # Doesn't work if last action was tap_twice. Needs something in between...?
        if self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action") == "tap_twice": # input_boolean.kitchen_lights_motion_override
            if self.get_state("sensor.xiaomi_cube_1_tap_twice_state") == self.light_list[0]:
                self.set_state("sensor.xiaomi_cube_1_tap_twice_state", state=self.light_list[1])
                self.turn_on(self.light_list[1],flash="short")
            elif self.get_state("sensor.xiaomi_cube_1_tap_twice_state") == self.light_list[1]:
                self.set_state("sensor.xiaomi_cube_1_tap_twice_state", state=self.light_list[2])
                self.turn_on(self.light_list[2],flash="short")
            elif self.get_state("sensor.xiaomi_cube_1_tap_twice_state") == self.light_list[2]:
                self.set_state("sensor.xiaomi_cube_1_tap_twice_state", state=self.light_list[0])
                self.turn_on(self.light_list[0],flash="short")

        # Can rotate be both clockwise and counterclockwise? I.e. both positive and negative integers?
        elif self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action")  == "rotate":
            # raw_value = self.get_state(self.args["entityID"], attribute = "action_value")
            # raw_value = self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action")
            raw_value = self.get_state("binary_sensor.cube_158d00028f7196", attribute = "value")
            action = self.get_state("binary_sensor.cube_158d00028f7196", data = "action_value")
            # dim_amount = {( int(255) * int(self.get_state(self.args["entityID"], attribute = "action_value") ) / int(360) )} # action value. Do I need to say self.get_state("binary_sensor.cube_158d00028f7196").action_value
            # new_brightness = self.get_state("sensor.xiaomi_cube_1_tap_twice_state").brightness + dim_amount
            # self.turn_on(self.get_state("sensor.xiaomi_cube_1_tap_twice_state"),brightness=new_brightness)
            self.log(raw_value)
            self.log(action)


# >
#         {%if trigger.event.data.action_value | float > 0 %}
#         {{  states.group.living_room_amb.attributes.brightness | int + 50 }}
#         {% else %}
#         {{  states.group.living_room_amb.attributes.brightness | int - 50 }}
#         {% endif %}



        # Turn active light to 100% brightness, 2200K.
        elif self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action") == "flip90":
            # if self.light_list[0]:
            #     self.turn_on("input_boolean.kitchen_lights_motion_override")
            self.turn_on(self.get_state("sensor.xiaomi_cube_1_tap_twice_state"), brightness=255, kelvin=2200)

        # Turn active light to 100% brightness, 2700K.
        elif self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action") == "flip180":
            # if self.light_list[0]:
            #     self.turn_on("input_boolean.kitchen_lights_motion_override")
            self.turn_on(self.get_state("sensor.xiaomi_cube_1_tap_twice_state"), brightness=255, kelvin=2700)

        # Turn off active light.
        elif self.get_state("binary_sensor.cube_158d00028f7196", attribute = "last_action") == "shake_air":
            # if self.light_list[0]:
            #     self.turn_off("input_boolean.kitchen_lights_motion_override")
            self.turn_off(self.get_state("sensor.xiaomi_cube_1_tap_twice_state"))

        # elif new == "move":
        #     if self.get_state(self.args["entity_1"]) == 'off':
        #         self.turn_on(self.args["entity_1"],brightness=255,kelvin=2700)
        #     else:
        #         self.turn_off(self.args["entity_1"])
