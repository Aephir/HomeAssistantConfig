"""
Xiaomi Aqara Magic Cube control
"""

import appdaemon.plugins.hass.hassapi as hass


class Remote(hass.Hass):


    def initialize(self):
        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])
        # Detect click. It detects sequential clicks of same button! (Why/how?)
        # self.listen_state(self.button_click,self.args["entityID"])


    def button_click(self, event_name, data, kwargs):
        """
        Sides are have numbers 1-6, side labeled "Aqara" is side #6
        data['event'] is either of type X00Y, where:

            X       = side it lands on
            Y       = side it came from
            Y       = 0 means moving while resting on side "X".
            7007    = shaking in air
            7008    = dropped (I think?)
            ????    = turn clockwise
            ????    = turn counterclockwise
            ????    = double tap
        """

        ninety      = [
            '1002', '1003', '1004', '1005', '2001', '2003', '2004', '2006',
            '3001', '3002', '3005', '3006', '4001', '4002', '4005', '4006',
            '5001', '5003', '5004', '5006', '6002', '6003', '6004', '6005'
            ]

        one_eighty  = [
            '1006', '2005', '3004', '4003', '5002', '6001'
            ]

        if data['id'] == self.args['id']: # Tap 1
            if data['event'] in ninety: # 90° turn
                self.toggle("switch.switch")
            # elif data['event'] in one_eighty: # 180° turn
            #     something
            # elif data['event'][1:] == '000' # Slide
            #     something
            # elif data['event'] == '7007': # Shake in air
            #     something
