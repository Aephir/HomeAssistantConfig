# Hue tap button

import appdaemon.plugins.hass.hassapi as hass

class HueRemote(hass.Hass):

    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.button_click,self.args["entityID"])

    def button_click(self, entity, attribute, old, new, kwargs):
        """
        "new" will be "1_click", "1_click_up", "1_hold", "1_hold_up", "2_click", etc.
        """
        if new == "1_click_up": # Toggle Dining Room Lights
            if self.get_state(self.args["entity_1"]) == 'off':
                self.turn_on(self.args["entity_1"],brightness=255,kelvin=2700)
            else:
                self.turn_off(self.args["entity_1"])
        elif new == "2_click_up": # Toggle Conservatory Lights
            if self.get_state(self.args["entity_2"]) == 'off':
                self.turn_on(self.args["entity_2"],brightness=255,kelvin=2700)
            else:
                self.turn_off(self.args["entity_2"])
        elif new == "3_click_up": # Toggle Kitchen Lights
            if self.get_state(self.args["entity_3"]) == 'off':
                self.turn_on(self.args["entity_3"],brightness=255,kelvin=2700)
            else:
                self.turn_off(self.args["entity_3"])
        elif new == "4_click_up": # Toggle Espresso Machine
            # self.toggle("switch.switch")
            self.toggle(self.args["entity_4"])
            # if self.get_state(self.args["entity_4"]) == 'off':
            #     self.turn_on(self.args["entity_4"])
            # else:
            #     self.turn_off(self.args["entity_4"])
        elif new == "1_hold": # Toggle Foutain
            if self.get_state(self.args["entity_5"]) == 'off':
                self.turn_on(self.args["entity_5"])
            else:
                self.turn_off(self.args["entity_5"])
        elif new == "2_hold": # Toggle Conservatory TV
            if self.get_state(self.args["entity_6"]) == 'off':
                self.turn_on(self.args["entity_6"])
            else:
                self.turn_off(self.args["entity_6"])
        # elif new == "3_hold":
        #     if self.get_state(self.args["entity_7"]) == 'off':
        #         self.turn_on(self.args["entity_7"],brightness=200,kelvin=2200)
        #     else:
        #         self.turn_off(self.args["entity_11"])
        # elif new == "4_hold": # input_boolean.kitchen_lights_motion_override
        #     if self.get_state(self.args["entity_8"]) == 'on':
        #         self.turn_off(self.args["entity_8"])
        #     else:
        #         self.turn_off(self.args["entity_12"])
        #         self.turn_off(self.args["entity_13"])
