import hassapi as hass
from datetime import datetime

class Routines(hass.Hass):

    def initialize(self):

        self.listen_state(self.who_and_when, 'sensor.aephir_s_vog_l29_next_alarm')


    def who_and_when(self, entity, attribute, old, new, kwargs):

        alarm_date  = self.get_state('sensor.aephir_s_vog_l29_next_alarm', attribute=date)
        now_date    = datetime.now().strftime('%Y-%m-%d')
        tomorrow    = (datetime.now() + .timedelta(days=1)).strftime('%Y-%m-%d')
        alarm_time  = self.get_state('sensor.aephir_s_vog_l29_next_alarm', attribute=time)
        now_time    = datetime.datetime.now().strftime('%H:%M')
        time_format = (datetime.now() + .timedelta(minutes=-10)).strftime('%H:%M')
        kids_up     = (datetime.now() + .timedelta(minutes=15)).strftime('%H:%M')

        adults      = ['device_tracker.meta_walden', 'device_tracker.meta_kristina']
        kids        = ['device_tracker.meta_emilie', 'device_tracker.meta_naia']


        if alarm_date == now_date and self.now_is_between('00:00', '09:00') or
            alarm_date == tomorrow and self.now_is_between('09:00', '00:00'):



            if any([True for adult in adults if self.get_state(adult) == 'home']):

                self.run_once(self.morning_routine, time_format)

            if any([True for kid in kids if self.get_state(kid) == 'home']):

                self.run_once(self.kids_morning, kids_up)

    def morning_routine(self):

        self.turn_on('switch.switch')
        self.turn_on('light.baby_room', brightness = 255, kelvin = 2700, transition=900)

    def kids_morning(self):

        self.turn_on('light.baby_room', brightness = 255, kelvin = 2700, transition=900)
        # Other lights
