

import appdaemon.plugins.hass.hassapi as hass
import datetime

class LightSlider(hass.Hass):

    def initialize(self):

        vacationMode = [
            'input_boolean.vacation_mode'
            ]

        deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        self.handle = self.run_at_sunset(self.homeAloneLights, 300, **kwargs)

        for device in deviceTrackers:
            self.listen_state(self.homeAloneLights, device)

        for entity in vacationMode:
            self.listen_state(self.homeAloneLights, entity)


    def someoneHome(self):
        home = 0
        for i in deviceTrackers:
            if self.get_state(i) == home:
                home += 1
        if home > 0:
            return True
        else:
            return False

    def homeAloneLights(self, entity, attribute, old, new, kwargs):

        if self.get_state('sun.sun') == 'below_horizon' and self.someoneHome() == False and self.get_state('input_boolean.vacation_mode') == 'on':
        

        self.handle = self.run_in(callback, 120, random_start = -60, **kwargs)
