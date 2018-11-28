# Script to track house occupancy.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Presence(hass.Hass):

    def initialize(self):

        # Device trackers to use
        deviceTrackers = [
        "device_tracker.meta_walden",
        # "device_tracker.meta_emilie",
        # "device_tracker.meta_naia",
        "input_boolean.guest_mode"
        "device_tracker.meta_kristina"
        ]

        for device in deviceTrackers:
            self.listen_state(occupancy,device)


    def whereIs(self, entity_id):
        return self.get_state(entity_id)

    def occupancy(self, entity_id):
        aephir = ''
        kristina = ''
        emilie = ''
        naia = ''
        guest_mode = ''


    def
