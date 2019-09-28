"""
Sends notification to Tasker about state changes
"""

import appdaemon.plugins.hass.hassapi as hass
import requests

class NotifyTasker(hass.Hass):

    def initialize(self):

        self.doors = [
            'binary_sensor.door_window_sensor_158d00022b3b66', # Basement door
            'binary_sensor.door_window_sensor_158d00022d0917', # Front door
            'binary_sensor.door_window_sensor_158d000234dc7b' # Conservatory door
            ]

        for entity in self.doors:
            self.listen_state(self.doorOpened, entity, new = 'on')


    def doorOpened (self, entity, attribute, old, new, kwargs):

        message = self.args['autoremote_url'] + 'latest_notification_is=:='

        if entity == 'binary_sensor.door_window_sensor_158d00022b3b66':
            message += 'Basement'
        elif entity == 'binary_sensor.door_window_sensor_158d00022d0917':
            message += 'Front'
        elif entity == 'binary_sensor.door_window_sensor_158d000234dc7b':
            message += 'Conservatory'

        requests.get(message)
