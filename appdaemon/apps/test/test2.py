# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import os

class Test(hass.Hass):


    def initialize(self):
        self.timer = None
        self.listen_state(self.test,"input_boolean.vacation_mode")

    def test(self, entity, attribute, old, new, kwargs):
        if new == 'on':
            self.timer = self.run_in(self.testAction, 3)
            # self.run_in(self.testAction, 3)
        else:
            self.cancel_timer(self.timer)

    def testAction(self, kwargs):

        self.toggle('light.conservatory_couch')
