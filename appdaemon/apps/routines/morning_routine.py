import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class Routines(hass.Hass):

    def initialize(self):

        self.listen_state(self.who_and_when, 'sensor.alarm_clock')


    def who_and_when(self, entity, attribute, old, new, kwargs):

        alarm_date  = self.get_state('sensor.alarm_clock', attribute=date)
        now_date    = datetime.now().strftime('%Y-%m-%d')
        tomorrow    = (datetime.now() + .timedelta(days=1)).strftime('%Y-%m-%d')
        alarm_time  = self.get_state('sensor.alarm_clock', attribute=time)
        now_time    = datetime.datetime.now().strftime('%H:%M')
        time_format = (datetime.now() + .timedelta(minutes=-10)).strftime('%H:%M')
        kids_up     = (datetime.now() + .timedelta(minutes=15)).strftime('%H:%M')

        if date == now_date and self.now_is_between('00:00', '09:00') or
            date == tomorrow and self.now_is_between('09:00', '00:00'):

            if self.get_state('device_tracker.meta_walden') == 'home':

                self.run_once(self.morning_routine, time_format)

            if self.get_state('device_tracker.meta_emilie') == 'home':

                self.run_once(self.kids_morning, kids_up)

    def morning_routine(self):

        self.turn_on('switch.switch')
        self.turn_on('light.baby_room', brightness = 255, kelvin = 2700, transition=900)
        # Might need to use call_service() instead.
        # E.g. self.call_service("light/turn_on", entity_id = "light.baby_room", brightness = 255, kelvin = 2700, transition = 900)

        requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')

    def kids_morning(self):

        self.turn_on('light.baby_room', brightness = 255, kelvin = 2700, transition=900)
        # Other lights
