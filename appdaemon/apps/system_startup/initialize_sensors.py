"""
Sets up my custom sensors at HASS startup if they don't exist.
Makes "Tasker" on phone send state, if present.
Sets sensor.alarm_clock to "none", if no alarm is set.
"""

import appdaemon.plugins.hass.hassapi as hass
import requests

class Initialization(hass.Hass):

    def initialize(self):

        entities = [
            'sensor.alarm_clock'
            # 'sensor.trash_pickup_date',
            # 'sensor.trash_pickup_type'
        ]

        for entity in entities:
            self.set_states(entity)


    def set_states(self, entity):

        if not self.entity_exists(entity):
            self.set_state(entity, state = 'none')
            message = self.args['autoremote_url'] + entity + '=:=none'
            requests.get(message)
