# Meta trackers combine data from multiple device_trackers.
# I re-wrote this to work in AppDaemon from https://github.com/arsaboo/homeassistant-config/blob/master/python_scripts/meta_device_tracker.py
# Notable changes:
# Router based location can only set to "home", not to "not_home", since a dead battery, or switching off wifi would make you "not_home".
# Added a few things to show [moving, driving, wifi_on, last_seen]
# Added support for using both life360 and google maps location (they have different names for the same thing, e.g. "battery" vs "battery_level")

import appdaemon.plugins.hass.hassapi as hass


class MetaTracker(hass.Hass):

    def initialize(self):

        # Set lists of trackers for each person.
        self.aephir_trackers = [
            self.args["aephir_maps_tracker"],
            self.args["aephir_l360_tracker"],
            self.args["aephir_ping_tracker"],
            self.args["aephir_bluetooth_1_tracker"]
            ]

        self.kristina_trackers = [
            self.args["kristina_ios_tracker"],
            self.args["kristina_l360_tracker"],
            self.args["kristina_ping_tracker"]
            ]

        self.emilie_trackers = [
            self.args["emilie_l360_tracker"],
            self.args["emilie_ping_tracker"]
            ]

        self.naia_trackers = [
            self.args["naia_ios_tracker"],
            self.args["naia_ping_tracker"],
            self.args["naia_l360_tracker"]
            ]

        self.meta_trackers = [
            "device_tracker.meta_emilie",
            "device_tracker.meta_kristina",
            "device_tracker.meta_naia",
            "device_tracker.meta_walden"
            ]

        pic = {
        "device_tracker.meta_emilie":"/local/images/emilie.jpg",
        "device_tracker.meta_kristina":"/local/images/kristina_3.jpg",
        "device_tracker.meta_naia":"/local/images/naia_2.jpg",
        "device_tracker.meta_walden":"/local/images/brain.jpg"
            }

        for tracker in self.meta_trackers:
            if not self.entity_exists(tracker):
                self.set_state(tracker, state = "Unknown", attributes = {'entity_picture':pic[tracker]})

        # Set list of all trackers.
        self.all_trackers = self.aephir_trackers + self.kristina_trackers + self.emilie_trackers + self.naia_trackers

        # Run "where_are_we" for any change in any tracker.
        for entity in self.all_trackers:
            self.listen_state(self.where_are_we, entity, attribute='all')

    def where_are_we(self, entity, attribute, old, new, kwargs):

        self.log("Tracker: ", str(entity))

        # Trackers
        aephir_trackers = [
            self.args["aephir_maps_tracker"],
            self.args["aephir_l360_tracker"],
            self.args["aephir_ping_tracker"],
            self.args["aephir_bluetooth_1_tracker"]
            ]

        kristina_trackers = [
            self.args["kristina_ios_tracker"],
            self.args["kristina_l360_tracker"],
            self.args["kristina_ping_tracker"]
            ]

        emilie_trackers = [
            self.args["emilie_l360_tracker"],
            self.args["emilie_ping_tracker"]
            ]

        naia_trackers = [
            self.args["naia_ios_tracker"],
            self.args["naia_ping_tracker"],
            self.args["naia_l360_tracker"]
            ]

        # Get entity that triggers script. I don't need this, this is "entity" that's passed from "initialize", right?
        triggeredEntity = entity

        # Variables to show in frontend
        newFriendlyName = ''
        newEntityPicture = ''
        metatrackerName = ''
        charging = ''
        driving = ''
        moving = ''
        raw_speed = ''
        speed = ''
        wifi_on = ''
        last_seen = ''

        # # Uncomment first time you run this to create meta device trackers in home assistant.
        # self.set_state('device_tracker.meta_walden', state='home')
        # self.set_state('device_tracker.meta_kristina', state='home')
        # self.set_state('device_tracker.meta_emilie', state='home')
        # self.set_state('device_tracker.meta_naia', state='home')

        # Set variables
        if triggeredEntity in aephir_trackers:
            newFriendlyName = 'Walden Meta Tracker'
            newEntityPicture = '/local/images/brain.jpg'
            metatrackerName = 'device_tracker.meta_walden'
        elif triggeredEntity in kristina_trackers:
            newFriendlyName = 'Kristina Meta Tracker'
            newEntityPicture = '/local/images/kristina_3.jpg'
            metatrackerName = 'device_tracker.meta_kristina'
        elif triggeredEntity in emilie_trackers:
            newFriendlyName = 'Emilie Meta Tracker'
            newEntityPicture = '/local/images/emilie.jpg'
            metatrackerName = 'device_tracker.meta_emilie'
        elif triggeredEntity in naia_trackers:
            newFriendlyName = 'Naia Meta Tracker'
            newEntityPicture = '/local/images/naia_2.jpg'
            metatrackerName = 'device_tracker.meta_naia'
        else:
            newFriendlyName = None
            metatrackerName = None


        # Get current meta tracker state new state from triggering tracker.
        newState = self.get_state(triggeredEntity)
        currentState = self.get_state(metatrackerName)

        # Get New data
        newSource = self.get_state(triggeredEntity, attribute = 'source_type')
        newFriendlyName_temp = self.get_state(triggeredEntity, attribute = 'friendly_name')

        # If router and "home", set to home no matter what. Disregard router state "not_home".
        if newSource == 'router' and new != 'home':
            newState = None

        # If router and "home", set to home no matter what. Disregard router state "not_home".
        if newSource == 'bluetooth' and new != 'home':
            newState = None

        # If GPS source, set new coordinates.
        if newSource == 'gps':
            newLatitude = self.get_state(triggeredEntity, attribute = 'latitude')
            newLongitude = self.get_state(triggeredEntity, attribute = 'longitude')
            newgpsAccuracy = self.get_state(triggeredEntity, attribute = 'gps_accuracy')
        elif self.get_state(metatrackerName, attribute = 'latitude') is not None:
            newLatitude = self.get_state(metatrackerName, attribute = 'latitude')
            newLongitude = self.get_state(metatrackerName, attribute = 'longitude')
            newgpsAccuracy = self.get_state(metatrackerName, attribute = 'gps_accuracy')
        else:
            newLatitude = None
            newLongitude = None
            newgpsAccuracy = None

        # Get Battery state
        if self.get_state(triggeredEntity, attribute = 'battery') is not None:
            newBattery = self.get_state(triggeredEntity, attribute = 'battery')
        elif self.get_state(triggeredEntity, attribute = 'battery_level') is not None:
            newBattery = self.get_state(triggeredEntity, attribute = 'battery_level')
        elif self.get_state(metatrackerName, attribute = 'battery') is not None:
            newBattery = self.get_state(metatrackerName, attribute = 'battery')
        else:
            newBattery = None
        if newBattery != None:
            newBattery = round(newBattery)

        # Get charging state
        if self.get_state(triggeredEntity, attribute = 'charging') is not None:
            newChargeState = self.get_state(triggeredEntity, attribute = 'charging')
        elif self.get_state(triggeredEntity, attribute = 'battery_charging') is not None:
            newChargeState = self.get_state(triggeredEntity, attribute = 'battery_charging')
        elif self.get_state(metatrackerName, attribute = 'charging') is not None:
            newChargeState = self.get_state(metatrackerName, attribute = 'charging')
        else:
            newChargeState = None

        # Get speed
        if self.get_state(triggeredEntity, attribute = 'speed') is not None:
            newVelocity = self.get_state(triggeredEntity, attribute = 'speed')
        elif self.get_state(metatrackerName, attribute = 'speed') is not None:
            newVelocity = self.get_state(metatrackerName, attribute = 'speed')
        else:
            newVelocity = None

        # Get driving state
        if self.get_state(triggeredEntity, attribute = 'driving') is not None:
            newDriveState = self.get_state(triggeredEntity, attribute = 'driving')
        elif self.get_state(metatrackerName, attribute = 'driving') is not None:
            newDriveState = self.get_state(metatrackerName, attribute = 'driving')
        else:
            newDriveState = None

        # Get moving state
        if self.get_state(triggeredEntity, attribute = 'moving') is not None:
            newMoveState = self.get_state(triggeredEntity, attribute = 'moving')
        elif self.get_state(metatrackerName, attribute = 'moving') is not None:
            newMoveState = self.get_state(metatrackerName, attribute = 'moving')
        else:
            newMoveState = None

        # Get WiFi state
        if self.get_state(triggeredEntity, attribute = 'wifi_on') is not None:
            newWiFiState = self.get_state(triggeredEntity, attribute = 'wifi_on')
        elif self.get_state(metatrackerName, attribute = 'wifi_on') is not None:
            newWiFiState = self.get_state(metatrackerName, attribute = 'wifi_on')
        else:
            newWiFiState = None

        # Get last seen state
        if self.get_state(triggeredEntity, attribute = 'last_seen') is not None:
            newLastSeenTime = self.get_state(triggeredEntity, attribute = 'last_seen')
        elif self.get_state(metatrackerName, attribute = 'last_seen') is not None:
            newLastSeenTime = self.get_state(metatrackerName, attribute = 'last_seen')
        else:
            newLastSeenTime = None

        # Set new state, if applicable.
        if newState is not None:
            newStatus = newState
        else:
            newStatus = currentState


        # Create device_tracker.meta entity
        self.set_state(metatrackerName, state = newStatus, attributes = {
            'friendly_name': newFriendlyName,
            'entity_picture': newEntityPicture,
            'source_type': newSource,
            'battery': newBattery,
            'gps_accuracy': newgpsAccuracy,
            'latitude': newLatitude,
            'longitude': newLongitude,
            'velocity': newVelocity,
            'update_source': triggeredEntity,
            # 'custom_ui_state_card': 'state-card-custom-ui',
            'show_last_changed': 'true',
            'charging': newChargeState,
            'driving': newDriveState,
            'wifi_on': newWiFiState,
            'moving': newMoveState,
            'last_seen': str(newLastSeenTime)
            }
        )
