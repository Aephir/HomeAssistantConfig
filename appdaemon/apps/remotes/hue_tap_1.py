# Motion sensors to control the main floor bathroom lights

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class HueRemote(hass.Hass):

    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.button_click,"sensor.bedroom_switch")

    def button_click(self, entity, attribute, old, new, kwargs):
        # button will be "1_click", "2_click", etc.
        button = self.get_state("sensor.bedroom_switch")
        if button == "1_click":
            self.toggle("switch.fountain")
        elif button == "2_click":
            self.turn_on("light.conservatory_lights")
        elif button == "3_click":
            self.turn_on("light.dining_room_lights")
        elif button == "4_click":
            self.turn_off("light.conservatory_lights")
        # self.set_state("sensor.bedroom_switch", state = "idle")
