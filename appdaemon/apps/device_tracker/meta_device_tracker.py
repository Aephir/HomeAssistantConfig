# Combine multiple device trackers into one entity
# You can call the script using the following:
# - service: python_script.meta_device_tracker
#   data_template:
#     entity_id: '{{trigger.entity_id}}'


import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MetaTracker(hass.Hass):

    def initialize(self):
        # Aephir trackers
        self.listen_state(self.whereAreWe,self.args["aephir_maps_tracker"])
        self.listen_state(self.whereAreWe,self.args["aephir_l360_tracker"])
        self.listen_state(self.whereAreWe,self.args["aephir_ping_tracker"])
        # Kristina trackers
        self.listen_state(self.whereAreWe,self.args["kristina_ios_tracker"])
        self.listen_state(self.whereAreWe,self.args["kristina_l360_tracker"])
        self.listen_state(self.whereAreWe,self.args["kristina_ping_tracker"])
        # Emilie trackers
        self.listen_state(self.whereAreWe,self.args["emilie_l360_tracker"])
        self.listen_state(self.whereAreWe,self.args["emilie_ping_tracker"])
        # Naia trackers
        self.listen_state(self.whereAreWe,self.args["naia_ios_tracker"])
        self.listen_state(self.whereAreWe,self.args["naia_ping_tracker"])


    def whereAreWe(self, entity, attribute, old, new, kwargs):

        # Trackers
        aephirTrackers = [
            self.args["aephir_maps_tracker"],
            self.args["aephir_l360_tracker"],
            self.args["aephir_ping_tracker"]
            ]
        kristinaTrackers = [
            self.args["kristina_ios_tracker"],
            self.args["kristina_l360_tracker"],
            self.args["kristina_ping_tracker"]
            ]
        emilieTrackers = [
            self.args["emilie_l360_tracker"],
            self.args["emilie_ping_tracker"]
            ]
        naiaTrackers = [
            self.args["naia_ios_tracker"],
            self.args["naia_ping_tracker"]
            ]

        # Get entity that triggers script
        triggeredEntity = self.get_entity('entity_id')

        # Variables to show in frontend
        newFriendlyNam = ''
        newEntityPicture = ''
        metatrackerName = ''

        # Set variables
        if triggeredEntity in aephirTrackers:
            newFriendlyName = 'Walden Meta Tracker'
            newEntityPicture = '/local/images/brain.jpg'
            metatrackerName = 'device_tracker.meta_walden'
        elif triggeredEntity in kristinaTrackers:
            newFriendlyName = 'Kristina Meta Tracker'
            newEntityPicture = '/local/images/kristina_v2.jpg'
            metatrackerName = 'device_tracker.meta_kristina'
        elif triggeredEntity in emilieTrackers:
            newFriendlyName = 'Emilie Meta Tracker'
            newEntityPicture = '/local/images/emilie.jpg'
            metatrackerName = 'device_tracker.meta_emilie'
        elif triggeredEntity in naiaTrackers:
            newFriendlyName = 'Naia Meta Tracker'
            newEntityPicture = '/local/images/naia_2.jpg'
            metatrackerName = 'device_tracker.meta_naia'
        else:
            newFriendlyName = None
            metatrackerName = None


        # Get current & new state
        newState = self.get_state(triggeredEntity)
        currentState = self.get_state(metatrackerName)
        # Get New data
        newSource = self.get_state(triggeredEntity, state = newState, attribute = 'source_type')
        newFriendlyName_temp = self.get_state(triggeredEntity, state = newState, attribute = 'friendly_name')

        # If GPS source, set new coordinates
        if newSource == 'gps':
            newLatitude = self.get_state(triggeredEntity, state = newState, attribute = 'latitude')
            newLongitude = self.get_state(triggeredEntity, state = newState, attribute = 'longitude')
            newgpsAccuracy = self.get_state(triggeredEntity, state = newState, attribute = 'gps_accuracy')
        # If not, keep last known coordinates
        elif currentState.get_state(attribute = 'latitude') is not None:
            newLatitude = self.get_state(metatrackerName, state = currentState, attribute = 'latitude')
            newLongitude = self.get_state(metatrackerName, state = currentState, attribute = 'longitude')
            newgpsAccuracy = self.get_state(metatrackerName, state = currentState, attribute = 'gps_accuracy')
        # Otherwise return null
        else:
            newLatitude = None
            newLongitude = None
            newgpsAccuracy = None

        # Get Battery
        if self.get_state(triggeredEntity, state = newState, attribute = 'battery') is not None:
            newBattery = newState.get_state(attribute = 'battery')
        elif self.get_state(metatrackerName, state = currentState, attribute = 'battery') is not None:
            newBattery = currentState.get_state(attribute = 'battery')
        else:
            newBattery = None

        # Get velocity
        if self.get_state(triggeredEntity, state = newState, attribute = 'velocity') is not None:
            newVelocity = newState.get_state(attribute = 'velocity')
        elif self.get_state(metatrackerName, state = currentState, attribute = 'velocity') is not None:
            newVelocity = currentState.get_state(attribute = 'velocity')
        else:
            newVelocity = None

        if newState.state is not None:
            newStatus = newState.state
        else:
            newStatus = currentState.state

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
            'custom_ui_state_card': 'state-card-custom-ui',
            'show_last_changed': 'true'
        })
