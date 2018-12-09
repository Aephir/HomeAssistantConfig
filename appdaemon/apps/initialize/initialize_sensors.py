# Sensors to create as home assistant restart (if they don't exist)

import appdaemon.plugins.hass.hassapi as hass

class Initialize(hass.Hass):

    def initialize(self):

        self.device_trackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina',
            'device_tracker.meta_emilie',
            'device_tracker.meta_naia'
            ]

        for entity in self.device_trackers:
            if not self.entity_exists(entity):
                self.set_state(entity, state="Unknown")
