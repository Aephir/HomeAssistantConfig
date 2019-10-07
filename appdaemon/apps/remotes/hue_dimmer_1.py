# Hue tap button

import appdaemon.plugins.hass.hassapi as hass

class Remote(hass.Hass):

    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])
        # self.listen_state(self.button_click,self.args["id"])

    def button_click(self, event_name, data, kwargs):
        """
        data['event'] is in the format 'X00Y', where:

            X is button number
            Y is action. If Y is:
                0   = button down
                1   = button hold
                2   = button up
                3   = Button hold up
        """

        if data['id'] == self.args['id']: # Dimmer Switch 1
            if data['event'] == 1002: # Button 1 up
                if self.get_state(self.args["entity_1"]) == 'off':
                    self.turn_on(self.args["entity_1"],brightness=255,kelvin=2700)
                else:
                    self.turn_off(self.args["entity_1"])
            elif data['event'] == 2002: # Button 2 up
                if self.get_state(self.args["entity_2"]) == 'off':
                    self.turn_on(self.args["entity_2"],brightness=255,kelvin=2700)
                else:
                    self.turn_off(self.args["entity_2"])
            elif data['event'] == 3002: # Button 3 up
                if self.get_state(self.args["entity_3"]) == 'off':
                    self.turn_on(self.args["entity_3"],brightness=255,kelvin=2700)
                else:
                    self.turn_off(self.args["entity_3"])
            elif data['event'] == 4002: # Button 4 up
                # if self.get_state(self.args["entity_4"]) == 'on':
                #     self.turn_off(self.args["entity_4"])
                # elif self.get_state(self.args["entity_4"]) == 'off':
                #     self.turn_off(self.args["entity_4"])
                self.toggle(self.args["entity_4"])
            elif data['event'] == 1001: # Button 1 hold
                if self.get_state(self.args["entity_5"]) == 'off':
                    self.turn_on(self.args["entity_5"])
                else:
                    self.turn_off(self.args["entity_5"])
            elif data['event'] == 2001: # Button 2 hold
                if self.get_state(self.args["entity_6"]) == 'off':
                    self.turn_on(self.args["entity_6"])
                else:
                    self.turn_off(self.args["entity_6"])

        # if new == "1_click_up": # Toggle Dining Room Lights
        #     if self.get_state(self.args["entity_1"]) == 'off':
        #         self.turn_on(self.args["entity_1"],brightness=255,kelvin=2700)
        #     else:
        #         self.turn_off(self.args["entity_1"])
        # elif new == "2_click_up": # Toggle Conservatory Lights
        #     if self.get_state(self.args["entity_2"]) == 'off':
        #         self.turn_on(self.args["entity_2"],brightness=255,kelvin=2700)
        #     else:
        #         self.turn_off(self.args["entity_2"])
        # elif new == "3_click_up": # Toggle Kitchen Lights
        #     if self.get_state(self.args["entity_3"]) == 'off':
        #         self.turn_on(self.args["entity_3"],brightness=255,kelvin=2700)
        #     else:
        #         self.turn_off(self.args["entity_3"])
        # elif new == "4_click_up": # Toggle Espresso Machine
        #     # self.toggle("switch.switch")
        #     self.toggle(self.args["entity_4"])
        #     # if self.get_state(self.args["entity_4"]) == 'off':
        #     #     self.turn_on(self.args["entity_4"])
        #     # else:
        #     #     self.turn_off(self.args["entity_4"])
        # elif new == "1_hold": # Toggle Foutain
        #     if self.get_state(self.args["entity_5"]) == 'off':
        #         self.turn_on(self.args["entity_5"])
        #     else:
        #         self.turn_off(self.args["entity_5"])
        # elif new == "2_hold": # Toggle Conservatory TV
        #     if self.get_state(self.args["entity_6"]) == 'off':
        #         self.turn_on(self.args["entity_6"])
        #     else:
        #         self.turn_off(self.args["entity_6"])
        # # elif new == "3_hold":
        # #     if self.get_state(self.args["entity_7"]) == 'off':
        # #         self.turn_on(self.args["entity_7"],brightness=200,kelvin=2200)
        # #     else:
        # #         self.turn_off(self.args["entity_11"])
        # # elif new == "4_hold": # input_boolean.kitchen_lights_motion_override
        # #     if self.get_state(self.args["entity_8"]) == 'on':
        # #         self.turn_off(self.args["entity_8"])
        # #     else:
        # #         self.turn_off(self.args["entity_12"])
        # #         self.turn_off(self.args["entity_13"])
