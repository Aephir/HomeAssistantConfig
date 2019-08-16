"""
Sets up my custom sensors at HASS startup if they don't exist.
Makes "Tasker" on phone send state, if present.
Sets sensor.alarm_clock to "none", if no alarm is set.
"""

import appdaemon.plugins.hass.hassapi as hass
import requests


class Initialization(hass.Hass):

    def initialize(self):

        self.log("Hello from Initialize")

        entities = [
            'sensor.alarm_clock'
            # 'sensor.trash_pickup_date',
            # 'sensor.trash_pickup_type'
        ]

        for entity in entities:
            self.set_states(entity)


    def set_states(self, entity):

        try:
            self.get_state(entity)
        except:
            self.set_state(entity, state = 'none')
            message = 'https://autoremotejoaomgcd.appspot.com/sendmessage?key=APA91bHdG9gIIRophSN4rAlk4Y23LJa9o4KH_Q4I44Fzzf3luTHuOITsn0wOwZg3OhfdiPYsjYgWST8ckLapuJPjcHmY4y9G1cHOW96otuGr4M-irV57GXOHP4dC9QVNGcDOckZk2A45&message=' + entity + '=:=none'
            requests.get(message)

        if entity == 'sensor.alarm_clock':
            self.run_in(self.na_state, 10)

    def na_state(self):

        self.set_state('sensor.alarm_clock', state = 'none')
