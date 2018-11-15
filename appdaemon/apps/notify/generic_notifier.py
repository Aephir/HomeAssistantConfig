# Generic notifier.
# Use self.set_state("sensor.notify_message", state="blabla") from any other app
# See https://community.home-assistant.io/t/a-notify-function-that-does-more-then-just-1-notify/32483

import appdaemon.plugins.hass.hassapi as hass


class notify(hass.Hass):

    def initialize(self):
        # Send this from another app using self.set_state("sensor.notify_message", state="blabla"). "state" = message.
        self.set_state("sensor.notify_message",state=" ")
        # Send this from another app using self.set_state("sensor.notify_message", state="['notify/home_aephir_bot','notify/ios_kristinas_iphone']"). "state" = notifiers.
        # or state=['notify/home_aephir_bot','notify/ios_kristinas_iphone'] ??
        # e.g.
        self.set_state("sensor.notify_ids",state=" ")
        self.listen_state(self.send_notify,"sensor.notify_message")
        notifier_ids = self.get_state("sensor.notify_ids")


    def send_notify(self, entity, attribute, old, new, kwargs):
        for notifier in notifier_ids:
            self.call_service(notifier,message=new)
        self.log(new)
    ... do any action you like when a meassage is send, send messages to several notifiers
    ... use tts to hear the message, translate the message, anything you can think off
