# Manual override of kitchen motion controlled lights

import appdaemon.plugins.hass.hassapi as hass

class ManualOverride(hass.Hass):

    def initialize(self):
        self.listen_state(SwitchInputBooleanOn,self.args["entity"], new="4_click_up")
        self.listen_state(SwitchInputBooleanOff,self.args["entity"], new="4_hold")

    def SwitchInputBooleanOn(self, entity, attribute, old, new, kwargs):
        self.turn_on(self.args["entity"])

    def SwitchInputBooleanOff(self, entity, attribute, old, new, kwargs):
        self.turn_off(self.args["entity"])
