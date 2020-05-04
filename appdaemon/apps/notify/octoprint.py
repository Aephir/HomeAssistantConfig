import appdaemon.plugins.hass.hassapi as hass
import datetime


class Notify(hass.Hass):

    def initialize(self):

        self.listen_state(self.notify_octoprint_status, 'sensor.prusa_i3_mk3s_current_state', old = 'Printing')


    def notify_octoprint_status(self, entity, attribute, old, new, kwargs):

        notify  = False
        message = ''

        if self.get_state('binary_sensor.prusa_i3_mk3s_printing_error') == 'on':
            notify  = True
            message = 'Printer Error!'
        elif self.get_state(' sensor.prusa_status') == 'Idle':
            notify  = True
            message = 'Print Complete!'

        if message != '':
            self.call_service('notify/home_aephir_bot', message=message)
