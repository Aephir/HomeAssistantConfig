# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import os

class Test(hass.Hass):


    def initialize(self):

        self.listen_state(self.test,"input_boolean.vacation_mode")

    def test(self, entity, attribute, old, new, kwargs):

        # self.log("test2")

        test = self.get_app("global_function_test")
        classtoget = test.global_functions()
        func = classtoget.AreWeAwake("light.dining_room_lights")

        self.log(test)
        self.log(classteget)
        self.log(func)

        if func:
            self.toggle("light.baby_room")
