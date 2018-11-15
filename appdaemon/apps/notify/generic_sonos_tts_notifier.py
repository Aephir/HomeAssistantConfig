# Generic notifier.
# Use self.set_state("sensor.notify_message", state="blabla") from any other app
# See https://community.home-assistant.io/t/a-notify-function-that-does-more-then-just-1-notify/32483

import appdaemon.plugins.hass.hassapi as hass


class notify(hass.Hass):

  def initialize(self):
    self.set_state("sensor.notify_message",state=" ")
    self.listen_state(self.send_notify,"sensor.notify_message")

  def send_notify(self, entity, attribute, old, new, kwargs):
    self.call_service("notify/pushetta",message=new)
    self.log(new)
    ... do any action you like when a meassage is send, send messages to several notifiers
    ... use tts to hear the message, translate the message, anything you can think off


self.set_state("sensor.notify_message", state="blabla")
