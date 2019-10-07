"""
Script to determine whether or not we are awake.
It will only set us as "awake" if we are also home.
It has a 15 minute delay from we are in bed to it thinks we are going to sleep.
"""

import appdaemon.plugins.hass.hassapi as hass

class Awake(hass.Hass):

    def initialize(self):

        # Set up timers like this?
        # https://github.com/ai3xbe/Home_Assistant_public/blob/4bc98b8ba75c22017e694367b46a89319e889e53/AppDaemon/presence.py
        self.aephir_timer   = self.run_in(self.awake, 5)
        self.kristina_timer = self.run_in(self.awake, 5)
        self.cancel_timer(self.aephir_timer)
        self.cancel_timer(self.kristina_timer)

        in_bed          = [
            'binary_sensor.aephir_in_bed',
            'binary_sensor.kristina_in_bed'
            ]

        booleans        = [
            'input_boolean.party_mode'
            ]

        meta_trackers   = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        for sensor in in_bed:
            self.listen_state(self.timer_func, sensor)

        # for tracker in meta_trackers:
        #     self.listen_state(self.trackers, tracker)

    def trackers(self, entity, attribute, old, new, kwargs):

        try:
            self.get_state('sensor.awake')
        except:
            self.awake()


    def timer_func(self, entity, attribute, old, new, kwargs):

        self.log("Timer func running")

        ### Get from "global_functions.py -> workday_when_waking"



        if self.get_state('input_boolean.vacation_mode') == 'off':
            self.log('One')
            if self.now_is_between("20:30:00", "00:00:00"):
                self.log('Two')
                night_time = self.get_state('binary_sensor.workday_tomorrow') == 'on'
            elif self.now_is_between("00:00:00", "08:00:00"):
                self.log('Three')
                night_time = self.get_state('binary_sensor.workday_today') == 'on'
            else:
                night_time = False
        else:
            self.log('Four')
            night_time = self.now_is_between("20:30:00", "09:00:00")

        self.log("is it night time?")
        self.log(night_time)

        if night_time:
            if entity == 'binary_sensor.aephir_in_bed':
                self.cancel_timer(self.aephir_timer)
                self.aephir_timer = self.run_in(self.awake, 5) #900
            elif entity == 'binary_sensor.kristina_in_bed':
                self.cancel_timer(self.kristina_timer)
                self.log('Kristina bed')
                self.kristina_timer = self.run_in(self.awake, 5) #900
        else:
            who_is_home = ''
            if self.get_state('device_tracker.meta_walden') == 'home':
                who_is_home += 'Walden, '
            if self.get_state('device_tracker.meta_kristina') == 'home':
                who_is_home += 'Kristina, '
            who_is_awake = who_is_awake[:len(who_is_awake)-2]
            self.set_state('sensor.awake', state = 'on', attributes = {
                'who_is_awake': who_is_awake})

    def awake(self, kwargs):

        anyone_awake = 'off'
        who_is_awake = ''

        self.log('self.run_in working') # No, it is not working!!

        if self.get_state('device_tracker.meta_walden') == 'home' and self.get_state('binary_sensor.aephir_in_bed') == 'off':
            who_is_awake   += 'Walden, '
            anyone_awake    = 'on'

        if self.get_state('device_tracker.meta_kristina') == 'home' and self.get_state('binary_sensor.kristina_in_bed') == 'off':
            who_is_awake   += 'Kristina, '
            anyone_awake    = 'on'

        who_is_awake    = who_is_awake[:len(who_is_awake)-2]
        # if self.get_state('input_boolean.guest_mode') == 'on':

        self.set_state('sensor.awake', state = anyone_awake, attributes = {
            'who_is_awake': who_is_awake
        })
