"""
Hue tap button setup.
Control fountain, conservatory lights, dining room lights, and media players (audio).
"""

import appdaemon.plugins.hass.hassapi as hass


class HueRemote(hass.Hass):


    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        self.listen_state(self.button_click,self.args["entityID"])


    def button_click(self, entity, attribute, old, new, kwargs):
        # "self" will be "1_click", "2_click", etc.
        if new == "1_click":
            self.toggle("switch.fountain")
        elif new == "2_click":
            self.toggle("light.conservatory_lights")
        elif new == "3_click":
            self.toggle("light.dining_room_lights")
        elif new == "4_click":
            if any(self.args["entity_4"] == "playing"):
                for entity in self.args["entity_4"]:
                    self.call_service("media_player.media_pause",entity)
            elif any(self.args["entity_4"] == "paused"):
                for entity in self.args["entity_4"]:
                    self.call_service("media_player.media_play",entity)
