# Motion sensors to control the main floor bathroom lights

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class HueRemote(hass.Hass):

    def initialize(self):
        # Detect click
        self.listen_state(self.button_click,"sensor.bedroom_switch")

        # self.listen_state(self.button_click,"sensor.bedroom_switch", new="1_click")
        # self.listen_state(self.button_click,"sensor.bedroom_switch", new="2_click")
        # self.listen_state(self.button_click,"sensor.bedroom_switch", new="3_click")
        # self.listen_state(self.button_click,"sensor.bedroom_switch", new="4_click")

        # self.listen_state(self.button_click,"sensor.bedroom_switch" = "1_click", "2_click", "3_click", "4_click")

    def button_click(self, entity, attribute, old, new, kwargs):
        # Button will be "1_click", "2_click", etc.
        button = self.listen_state("sensor.bedroom_switch")
        if button == "1_click":
            self.toggle("switch.fountain")
        elif button == "2_click":
            self.turn_on("light.conservatory_lights")
        elif button == "3_click":
            self.turn_on("light.dining_room_lights")
        elif button == "4_click":
            self.turn_off("light.conservatory_lights")
        # self.set_state("sensor.bedroom_switch", state = "idle")
