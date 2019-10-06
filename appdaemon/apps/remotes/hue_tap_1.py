"""
Hue tap button setup.
Control fountain, conservatory lights, dining room lights, and media players (audio).
"""

import appdaemon.plugins.hass.hassapi as hass


class Remote(hass.Hass):


    def initialize(self):
        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        # self.listen_state(self.button_click,self.args["entityID"])


    def button_click(self, entity, attribute, old, new, kwargs):
        """
        data['event'] is either:

            34 = button 1
            16 = button 2
            17 = button 3
            18 = button 4
        """

        if data['id'] == self.args['id']: # Tap 1
            if data['event'] == 34: #
                self.toggle("switch.fountain")
            elif data['event'] == 16:
                self.toggle("light.conservatory_lights")
            elif data['event'] == 17:
                self.toggle("light.dining_room_lights")
            elif data['event'] == 18:
                if any(self.args["entity_4"] == "playing"):
                    for entity in self.args["entity_4"]:
                        self.call_service("media_player.media_pause",entity)
                elif any(self.args["entity_4"] == "paused"):
                    for entity in self.args["entity_4"]:
                        self.call_service("media_player.media_play",entity)


        # # "self" will be "1_click", "2_click", etc.
        # if new == "1_click":
        #     self.toggle("switch.fountain")
        # elif new == "2_click":
        #     self.toggle("light.conservatory_lights")
        # elif new == "3_click":
        #     self.toggle("light.dining_room_lights")
        # elif new == "4_click":
        #     if any(self.args["entity_4"] == "playing"):
        #         for entity in self.args["entity_4"]:
        #             self.call_service("media_player.media_pause",entity)
        #     elif any(self.args["entity_4"] == "paused"):
        #         for entity in self.args["entity_4"]:
        #             self.call_service("media_player.media_play",entity)
