# Warn me if the espresso machine is left "on" for more than 1 hour.

import appdaemon.plugins.hass.hassapi as hass
import time


class EspressoStatus(hass.Hass):

    def initialize(self):
        # Run SendNotification function if switch.switch has been on for 1 hour.
        self.listen_state(self.SendNotification0,"switch.switch", new="on", duration=3600) #3600

        # Run SendNotification function if switch.switch has been on for 1.5 hours.
        self.listen_state(self.SendNotification1,"switch.switch", new="on", duration=5400) #5400

        # Run SendNotification function if switch.switch has been on for 2 hours.
        self.listen_state(self.SendNotification2,"switch.switch", new="on", duration=7200) #7200


    # Send a notification to telegram
    def SendNotification0(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1 hour", data={"inline_keyboard":"Turn Off:/espresso_off, I Know:/removekeyboard"})
        self.log("Espresso machine has been on for 1 hour")

# [[["Turn off", "/espresso_off"], ["I know", "/removekeyboard"]]]

    # Send a notification to telegram
    def SendNotification1(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1.5 hours", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
        self.log("Espresso machine has been on for 1.5 hours")


    # Send a notification to telegram
    def SendNotification2(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 2 hours. I'm turning it off", data={"inline_keyboard":"Turn back on:/espresso_on, OK:/removekeyboard"})
        self.turn_off("switch.switch")
        self.log("Espresso machine has been on for 2 hours. Turning off")

'''
    def initialize(self):
        self.listen_event(self.telegram_callback_cb, "telegram_callback")
        self.call_service('telegram_bot/send_message', target = 111111, message = 'Try me', inline_keyboard = [[("Yes", "/yes"),("No", "/no")],  [("Maybe", "/maybe")]])

    def telegram_callback_cb(self, type, payload_event, kwargs):
        callback = payload_event["data"]
        user = payload_event["from_first"]
        self.log('Got "{}" from {}'.format(callback, user))
'''
