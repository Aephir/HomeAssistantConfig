import appdaemon.plugins.hass.hassapi as hass

class Alarm(hass.Hass):

    def initialize(self):

        requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')

# Dummy app config only with secrets.
# self.app_config['name_of_dummy_app']['secret_thing']