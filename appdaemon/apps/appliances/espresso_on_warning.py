# Warn me if the espresso machine is left "on" for more than 1 hour.

import appdaemon.plugins.hass.hassapi as hass
import time


class EspressoStatus(hass.Hass):

    def initialize(self):
        self.listen_state(self.SendNotification,"switch.switch", new="on", duration=3600)
        self.listen_state(self.SendNotification_2,"switch.switch", new="on", duration=5400)
        self.listen_state(self.SendNotification_3,"switch.switch", new="on", duration=7200)

    def SendNotification(self, entity, attribute, old, new, test, **kwargs):
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1 hour", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})

    def SendNotification_2(self, entity, attribute, old, new, test, **kwargs):
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1.5 hours", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})

    def SendNotification_3(self, entity, attribute, old, new, test, **kwargs):
        self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 2 hours", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})


'''
    def initialize(self):
        self.listen_event(self.telegram_callback_cb, "telegram_callback")
        self.call_service('telegram_bot/send_message', target = 111111, message = 'Try me', inline_keyboard = [[("Yes", "/yes"),("No", "/no")],  [("Maybe", "/maybe")]])

    def telegram_callback_cb(self, type, payload_event, kwargs):
        callback = payload_event["data"]
        user = payload_event["from_first"]
        self.log('Got "{}" from {}'.format(callback, user))
'''
