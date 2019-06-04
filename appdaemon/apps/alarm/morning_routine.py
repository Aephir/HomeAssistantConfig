"""
When alarm on phone is set, run a wake-up routine.
"""

import appdaemon.plugins.hass.hassapi as hass
import datetime

class Remote(hass.Hass):

    def initialize(self):

        self.alarm_time = None
        self.alarm_date = None

        self.listen_state(self.setUpIfHome, 'sensor.alarm_time')
        self.listen_state(self.setUpIfHome, 'device_tracker.meta_walden', new = 'home')


    def setUpIfHome(self, entity, attribute, old, new, kwargs):

        day_conversion = {
            'Monday':'0',
            'Tuesday':'1',
            'Wednesday':'2',
            'Thursday':'3',
            'Friday':'4',
            'Saturday':'5',
            'Sunday':'6'
            }

        self.alarm_time = datetime.time(int(str(self.get_state('sensor.alarm_time', attributes='alarm_time'))[:2]), int(str(self.get_state('sensor.alarm_time', attributes='alarm_time'))[3:]))
        self.alarm_date = day_conversion[self.get_state('sensor.alarm_time', attributes='alarm_date')]
        now = , datetime.datetime.now().hour) ':' str(datetime.datetime.now().minute)
        run_at_time = self.alarm_time - datetime.timedelta(minutes=15)

# int(str(self.get_state('sensor.alarm_time', attributes='alarm_time'))[:2])
# int(str(self.get_state('sensor.alarm_time', attributes='alarm_time'))[3:])

datetime.timedelta(minutes=15)

        if self.get_state('device_tracker.meta_walden') == 'home':

            self.run_at(self.morningRoutine, int(str(self.get_state('sensor.alarm_time', attributes='alarm_time'))[:2]), int(str(self.get_state('sensor.alarm_time', attributes='alarm_time'))[3:]))


    def morningRoutine(self, entity, attribute, old, new, kwargs):
