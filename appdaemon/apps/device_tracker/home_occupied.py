# Script to track house occupancy.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class HomeOccupancy(hass.Hass):

    def initialize(self):

        self.deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            # 'device_tracker.meta_emilie',
            # 'device_tracker.meta_naia',
            ]

        self.friendlyName = {
            'device_tracker.meta_walden': 'Walden',
            'device_tracker.meta_kristina': 'Kristina',
            'device_tracker.meta_emilie': 'Emilie',
            'device_tracker.meta_naia': 'Naia',
            'input_boolean.guest_mode': 'Guest'
            }

        self.anyHome = []

        self.occupancy(None)

        for entity in self.deviceTrackers:
            self.listen_state(self.occupancy, entity)


    def occupancy(self, entity):
        guest_mode = ''
        newStatus = ''
        numberOfPeople = 0

        self.anyHome = []

        for entity in self.deviceTrackers:
            if self.get_state(entity) == "home":
                self.anyHome.append(self.friendlyName[entity])
                numberOfPeople += 1
                newStatus = "Occupied"
            elif self.get_state('input_boolean.guest_mode') == 'on':
                newStatus = "Occupied"
            else:
                newStatus = "Unoccupied"

        if self.get_state('input_boolean.guest_mode') == "on":
            guest_mode == "on"
        else:
            guest_mode == "off"


        self.set_state('sensor.occupancy', state = newStatus, attributes = {
            'friendly_name': "Home occupancy",
            'number_of_people': numberOfPeople,
            'guests': guest_mode,
            'who_is_home': self.anyHome
            })
