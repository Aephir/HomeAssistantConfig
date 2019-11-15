# Script to track house occupancy.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Presence(hass.Hass):

    def initialize(self):

        # Device trackers to use
        deviceTrackers = [
        "device_tracker.meta_walden",
        "device_tracker.meta_kristina",
        "device_tracker.meta_emilie",
        # "device_tracker.meta_naia",
        "input_boolean.guest_mode"
        ]

        for device in deviceTrackers:
            self.listen_state(self.arriveHome, new = "home")

    # Check if anyone is home. Returns True/False.
    def occupancy(self, entity_id):
        aephir = 'device_tracker.meta_walden' == 'home'
        kristina = 'device_tracker.meta_kristina' == 'home'
        emilie = 'device_tracker.meta_emilie' == 'home'
        naia = 'device_tracker.meta_naia' == 'home'
        guest_mode = 'input_boolean.guest_mode' == 'on'
        anyoneHome = any([
            aephir,
            # naia,
            # emilia,
            kristina,
            guest_mode
            ])
        return anyoneHome


    def arriveHome(self, entity, attribute, old, new, kwargs):

        # Lists of entities to turn off.
        onList = [
        'light.all_lights',
        'switch.switch',
        'switch.fountain'
        # TVs and music...?
        ]

        # If "occupancy" returns 'False', then turn off all entities in offList, and notify the one who leaves last.
        if not self.occupancy:
            for entityID in offList:
                self.turn_off(entityID)
            if entity == 'device_tracker.meta_walden' or entity == 'input_boolean.guest_mode':
                self.call_service("notify/home_aephir_bot", message="The house is empty. I have turned off everything.", data={"inline_keyboard":"Turn espresso machine back on:/espresso_on, Thanks!:/removekeyboard"})
            elif entity == 'device_tracker.meta_kristina':
                self.call_service("notify/ios_kristinas_iphone", message="The house is empty. I have turned off everything.", data={"inline_keyboard":"Turn espresso machine back on:/espresso_on, Thanks!:/removekeyboard"})
