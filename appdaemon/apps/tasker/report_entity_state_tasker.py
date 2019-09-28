"""
Report state of entity to Tasker
"""

import appdaemon.plugins.hass.hassapi as hass
import requests

class NotifyTasker(hass.Hass):

    def initialize(self):

        self.entities = [
            self.args['entityID']
            ]

        for entity in self.entities:
            self.listen_state(self.reportState, entity)

    def reportState (self, entity, attribute, old, new, kwargs):

        message = self.args['autoremote_url'] + str(self.args['friendly_name']) + '_state_is=:=' + str(new)
        requests.get(message)
