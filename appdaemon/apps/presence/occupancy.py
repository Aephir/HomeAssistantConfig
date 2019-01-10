# Heating control

import appdaemon.plugins.hass.hassapi as hass


class HomeOccupancy(hass.Hass):

    def initialize(self):

        self.deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        # self.motionSensors = self.app_config['global_sensors']['motionSensors']

        for entity in self.deviceTrackers:
            self.listen_state(self.occupancy, entity)

        # for entity in self.motionSensors:
        #     self.listen_state(self.occupancy, entity)

        self.listen_state(self.occupancy, 'input_boolean.guest_mode')


    def occupancy(self, entity, attribute, old, new, kwargs):

        occupied = None
        who_is_home = []
        newStatus = None

        if self.get_state('device_tracker.meta_walden') == 'home':
            who_is_home.append('Walden')

        if self.get_state('device_tracker.meta_kristina') == 'home':
            who_is_home.append('Kristina')

        if self.get_state('device_tracker.meta_emile') == 'home':
            who_is_home.append('Emilie')

        if self.get_state('device_tracker.meta_walden') == 'home' or self.get_state('device_tracker.meta_kristina') == 'home':
            occupied = True
        else:
            occupied = False

        if occupied or self.get_state('input_boolean.guest_mode') == 'on':
            newStatus = 'on'
        else:
            newStatus = 'off'
        self.send(entity, attribute, old, new, occupied, who_is_home, newStatus, kwargs)

    def send(self, entity, attribute, old, new, occupied, who_is_home, newStatus, kwargs):
        self.set_state('sensor.home_occupancy', state = newStatus, attributes = {
            'friendly_name': 'Home occupancy',
            'guest_mode': self.get_state('input_boolean.guest_mode'),
            'who_is_home': who_is_home
            })
