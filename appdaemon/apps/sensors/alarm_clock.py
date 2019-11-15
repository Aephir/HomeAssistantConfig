import appdaemon.plugins.hass.hassapi as hass
import requests

class Alarm(hass.Hass):

    def initialize(self):

        requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
        self.listen_state('sensor.awake')

    def get_alarm(self, entity, attribute, old, new, kwargs):

        if new == 'off':
            requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
            
