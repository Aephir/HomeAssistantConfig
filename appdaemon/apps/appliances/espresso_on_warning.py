# Warn me if the espresso machine is left "on" for more than 45 minutes.
# Again if it is still on 3after 1 hour.
# After 1.5 hours, turn off and notify.

import appdaemon.plugins.hass.hassapi as hass
import time


class EspressoStatus(hass.Hass):

    def initialize(self):
        # Run SendNotification function if switch.switch has been on for 1 hour.
        self.listen_state(self.SendNotification0,"switch.switch", new="on", duration=2700) #2700 seconds = 0.75h

        # Run SendNotification function if switch.switch has been on for 1.5 hours.
        self.listen_state(self.SendNotification1,"switch.switch", new="on", duration=3600) #3600 seconds = 1h

        # Run SendNotification function if switch.switch has been on for 2 hours.
        self.listen_state(self.SendNotification2,"switch.switch", new="on", duration=5400) #5400 seconds = 1.5h


    # Send a notification to telegram
    def SendNotification0(self, entity, attribute, old, new, kwargs):
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 45 mins", data={"inline_keyboard":"Turn Off:/espresso_off, I Know:/removekeyboard"})
        self.log("Espresso machine has been on for 45 mins")

    # Send a notification to telegram
    def SendNotification1(self, entity, attribute, old, new, kwargs):
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1 hour", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
        self.log("Espresso machine has been on for 1 hour")

    # Send a notification to telegram
    def SendNotification2(self, entity, attribute, old, new, kwargs):
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1.5 hours. I'm turning it off", data={"inline_keyboard":"Turn back on:/espresso_on, OK:/removekeyboard"})
        self.turn_off("switch.switch")
        self.log("Espresso machine has been on for 1.5 hours. Turning off")
