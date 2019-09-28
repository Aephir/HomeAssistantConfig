import appdaemon.plugins.hass.hassapi as hass

class Alarm(hass.Hass):

    def initialize(self):

        requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
