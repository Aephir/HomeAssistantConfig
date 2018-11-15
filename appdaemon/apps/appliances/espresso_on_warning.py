# Warn me if the espresso machine is left "on" for more than 1 hour.

import appdaemon.plugins.hass.hassapi as hass
import time


class EspressoStatus(hass.Hass):

    def initialize(self):
        # Run SendNotification function if switch.switch has been on for 1 hour.
        self.listen_state(self.SendNotification,"switch.switch", new="on", duration=5) #3600

        # Run SendNotification function if switch.switch has been on for 1.5 hours.
        self.listen_state(self.SendNotification_2,"switch.switch", new="on", duration=12) #5400

        # Run SendNotification function if switch.switch has been on for 2 hours.
        self.listen_state(self.SendNotification_3,"switch.switch", new="on", duration=20) #7200


    # Send a notification to telegram
    def SendNotification(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1 hour", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
        self.log("Espresso machine has been on for 1 hour")

    def SendNotification_2(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1.5 hours", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
        self.log("Espresso machine has been on for 1.5 hours")

    def SendNotification_3(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 2 hours", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
        self.log("Espresso machine has been on for 2 hours")


'''
    def initialize(self):
        self.listen_event(self.telegram_callback_cb, "telegram_callback")
        self.call_service('telegram_bot/send_message', target = 111111, message = 'Try me', inline_keyboard = [[("Yes", "/yes"),("No", "/no")],  [("Maybe", "/maybe")]])

    def telegram_callback_cb(self, type, payload_event, kwargs):
        callback = payload_event["data"]
        user = payload_event["from_first"]
        self.log('Got "{}" from {}'.format(callback, user))
'''
