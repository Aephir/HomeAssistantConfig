# Hue tap button

import appdaemon.plugins.hass.hassapi as hass

class HueRemote(hass.Hass):

    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.button_click,self.args["entityID"])

    def button_click(self, entity, attribute, old, new, kwargs):
        # "button" will be "1_click", "2_click", etc.
        # I can remove the "button =" line, and just use "if new ==", right?
        button = self.get_state(self.args["entityID"])
        if button == "1_click":
            self.toggle("switch.fountain")
        elif button == "2_click":
            self.toggle("light.conservatory_lights")
        elif button == "3_click":
            self.toggle("light.dining_room_lights")
        elif button == "4_click":
            if any(self.args["entity_4"]) == "playing":
                self.call_service("media_player.media_pause",self.args["entity_4"])
            else:
            # elif all(self.args["entity_4"]) == "paused":
                self.call_service("media_player.media_play",self.args["entity_4"])
        # self.set_state("sensor.bedroom_switch", state = "idle")
