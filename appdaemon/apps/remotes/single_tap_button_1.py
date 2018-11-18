# Hue tap button

import appdaemon.plugins.hass.hassapi as hass

class Remote(hass.Hass):

    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.button_click,self.args["entityID"])

    def button_click(self, entity, attribute, old, new, kwargs):
        if self.now_is_between("06:00:00", "18:00:00"):
            self.turn_on(self.args["entityID1"])
        else:
            self.turn_off(self.args["entityID2"])
