# Script to track house occupancy.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Presence(hass.Hass):

    def initialize(self):

        # Device trackers to use
        self.deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina',
            'input_boolean.guest_mode'
            ]

        self.motionSensors = self.global_vars(self.motionSensors)

        self.locations = [
            "work_kristina",
            "work_walden",
            "off",
            "skole",
            "klubben"
            "central_copenhagen"
            ]

        self.weekday = ''
        self.comingLeaving = ''

        onOurWay = None

        self.listen_state(self.comingHome, "device_tracker.meta_kristina", old = "work_kristina", new = "away")
        self.listen_state(self.comingHome, "device_tracker.meta_walden", old = "work_walden", new = "away")
        self.listen_state(self.comingHome, "input_boolean.guest_mode", old = "off", new = "on")

        self.startTime = 15:30:00.000000
        self.endTime = 15:30:00.000000

    def comingOrLeaving(self, entity, attribute, old, new, kwargs):
        if self.occupancy() == False:
            self.comingLeaving = 'leaving'
        else:
            self.comingLeaving = 'coming'

    def anyOneHome(self, entity, attribute, old, new, kwargs):
        if self.get_state("device_tracker.meta_kristina") == 'home' or self.get_state("device_tracker.meta_walden") == 'home' or self.get_state("input_boolean.guest_mode") == 'on':
            return True
        elif self.get_state("device_tracker.meta_emilie") == 'home':
            return 'emilie'
        else:
            return False

    def comingHome(self, entity, attribute, old, new, kwargs):
        if self.comingLeaving == 'leaving':
            self.call_service() # Turn off thermostat.

        if datetime.datetime.today().weekday() 5:
            self.weekday = True

        if new == any[self.locations] and self.weekday:
            if self.now_is_between("15:00:00", "03:00:00"):
                self.call_service() # Set thermostat to $temp
                self.run_in(self.arrivedHome, 2700)


    def arrivedHome(self, entity, attribute, old, new, kwargs):
        if self.anyOneHome:
            self.get_state(device)


            self.call_service("notify/home_aephir_bot", message="No one came home. I'm turning the heat back off", data={"inline_keyboard":"Turn espresso machine back on:/espresso_on, Thanks!:/removekeyboard"})

    # Check if anyone is home. Returns True/False.
    def occupancy(self, entity_id):
        aephir = self.get_state('device_tracker.meta_walden') == 'home'
        kristina = self.get_state('device_tracker.meta_kristina') == 'home'
        emilie = self.get_state('device_tracker.meta_emilie') == 'home'
        naia = self.get_state('device_tracker.meta_naia') == 'home'
        guest_mode = self.get_state('input_boolean.guest_mode') == 'on'
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
        offList = [
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
