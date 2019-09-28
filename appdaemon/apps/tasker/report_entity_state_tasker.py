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

        message = 'https://autoremotejoaomgcd.appspot.com/sendmessage?key=APA91bHdG9gIIRophSN4rAlk4Y23LJa9o4KH_Q4I44Fzzf3luTHuOITsn0wOwZg3OhfdiPYsjYgWST8ckLapuJPjcHmY4y9G1cHOW96otuGr4M-irV57GXOHP4dC9QVNGcDOckZk2A45&message=' + str(self.args['friendly_name']) + '_state_is=:=' + str(new)
        requests.get(message)
