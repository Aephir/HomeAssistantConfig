# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import os

class Test(hass.Hass):


    def initialize(self):
        # Run SendNotification function if switch.switch has been on for 1 hour.
        self.listen_state(self.test,"input_boolean.vacation_mode", new="on") #3600

    # Send a notification to telegram
    def test(self, entity, attribute, old, new, kwargs):
        os.system("shutdown /r /t 1") # shutdown and reboot (/r) in time (/t) = 1 second (1)
        self.log("I tried to reboot")
