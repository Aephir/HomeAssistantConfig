# Script to track house occupancy.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Presence(hass.Hass):

    def initialize(self):

        self.device_trackers = [
            'device_tracker.meta_emilie',
            # 'device_tracker.meta_naia',
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        self.friendly_name = {
            'device_tracker.meta_walden': 'Walden',
            'device_tracker.meta_kristina': 'Kristina',
            'device_tracker.meta_emilie': 'Emilie',
            'device_tracker.meta_naia': 'Naia',
            'input_boolean.guest_mode': 'Guest'
            }

        self.occupancy(None, None, None, None, None)

        for entity in self.device_trackers:
            self.listen_state(self.occupancy, entity)


    def occupancy(self, entity, attributes, old, new, kwargs):

        guest_mode = ''
        new_status = ''
        number_of_people = 0

        who_is_home = []

        for e in self.device_trackers:

            if self.get_state(e) == "home":
                who_is_home.append(self.friendly_name[e])
                number_of_people += 1
                new_status = "Occupied"

        if self.get_state('input_boolean.guest_mode') == 'on':
            new_status = "Occupied"
        elif number_of_people == 0:
            new_status = "Unoccupied"

        if self.get_state('input_boolean.guest_mode') == "on":
            guest_mode == "on"
        else:
            guest_mode == "off"

        self.set_state('sensor.occupancy', state = new_status, attributes = {
            'friendly_name': "Home occupancy",
            'known_people': number_of_people,
            'guests': guest_mode,
            'who_is_home': who_is_home
            })
