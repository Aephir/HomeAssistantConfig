# Hue tap button

import appdaemon.plugins.hass.hassapi as hass

class Remote(hass.Hass):

    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])

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

        awake = True # Make the "Awake" sensor.

        if awake:
            brightness = 255
        else:
            brightness = 100

        if data['id'] == self.args['id']: # Dimmer Switch 1
            if data['event'] == 1002: # Button 1 up
                self.turn_on(self.args["entity_3"],brightness=brightness,kelvin=2700)
            elif data['event'] == 2002: # Button 2 up
                if self.get_state(self.args["entity_1"]) == 'off':
                    self.turn_on(self.args["entity_1"],brightness=brightness,kelvin=2700)
                else:
                    self.turn_off(self.args["entity_1"])
            elif data['event'] == 3002: # Button 3 up
                if self.get_state(self.args["entity_2"]) == 'off':
                    self.turn_on(self.args["entity_2"],brightness=brightness,kelvin=2700)
                else:
                    self.turn_off(self.args["entity_2"])
            elif data['event'] == 4002: # Button 4 up
                self.turn_off(self.args["entity_3"])
            elif data['event'] == 3002: # Button 1 hold up
                self.turn_on(self.args["entity_3"],brightness=255,kelvin=2700)
