"""
Hue tap button setup.
Control fountain, conservatory lights, dining room lights, and media players (audio).
"""

import appdaemon.plugins.hass.hassapi as hass

class Remote(hass.Hass):

    def initialize(self):

        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])


    def button_click(self, event_name, data, kwargs):
        """
        data['event'] is either:

            34 = button 1
            16 = button 2
            17 = button 3
            18 = button 4

        """
        self.log('testing')

        if data['id'] == self.args['id']: # Tap 1
            if data['event'] == 34:     # Button 1
                self.toggle(self.args['entity_1'])
            elif data['event'] == 16:   # Button 2
                self.toggle(self.args['entity_2'])
            elif data['event'] == 17:   # Button 3
                self.toggle(self.args['entity_3'])
            elif data['event'] == 18:   # Button 4
                self.toggle(self.args['entity_4'])


            #     if any(self.args["entity_4"] == "playing"):
            #         for entity in self.args["entity_4"]:
            #             self.call_service("media_player.media_pause",entity)
            #     elif any(self.args["entity_4"] == "paused"):
            #         for entity in self.args["entity_4"]:
            #             self.call_service("media_player.media_play",entity)
