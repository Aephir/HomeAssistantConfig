# Generic notifier.
# Use self.set_state("sensor.notify_message", state="blabla") from any other app
# See https://community.home-assistant.io/t/a-notify-function-that-does-more-then-just-1-notify/32483

import appdaemon.plugins.hass.hassapi as hass


class Notify(hass.Hass):

    def initialize(self):

        self.listen_state(self.send_notify,'sensor.trash_pickup')


    def send_notify(self, entity, attribute, old, new, kwargs):

        trashtype   = str(self.get_state('sensor.trash_pickup', attribute='trash_type'))[:-1]
        trashdate   = str(self.get_state('sensor.trash_pickup', attribute='trash_date'))[:-1]
        trashday    = str(self.get_state('sensor.trash_pickup', attribute='trash_day'))[:-1]

        self.call_service('notify/home_aephir_bot', message='På ' + trashday + ' d. ' + trashdate + ' bliver der hentet ' + trashtype + '.\n\nHusk at stille affaldet ud!!')
        self.call_service("notify/ios_kristinas_iphone", message='På ' + trashday + ' d. ' + trashdate + ' bliver der hentet ' + trashtype + '.\n\nHusk at stille affaldet ud!!')
