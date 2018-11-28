# Meta trackers combine data from multiple device_trackers.
# I re-wrote this to work in AppDaemon from https://github.com/arsaboo/homeassistant-config/blob/master/python_scripts/meta_device_tracker.py

# Combine multiple device trackers into one entity
# You can call the script using the following:
# - service: python_script.meta_device_tracker
#   data_template:
#     entity_id: '{{trigger.entity_id}}'


import appdaemon.plugins.hass.hassapi as hass


class MetaTracker(hass.Hass):

    def initialize(self):

        # Set lists of trackers for each person.
        self.aephirTrackers = [
            self.args["aephir_maps_tracker"],
            self.args["aephir_l360_tracker"],
            self.args["aephir_ping_tracker"]
            ]

        self.kristinaTrackers = [
            self.args["kristina_ios_tracker"],
            self.args["kristina_l360_tracker"],
            self.args["kristina_ping_tracker"]
            ]

        self.emilieTrackers = [
            self.args["emilie_l360_tracker"],
            self.args["emilie_ping_tracker"]
            ]

        self.naiaTrackers = [
            self.args["naia_ios_tracker"],
            self.args["naia_ping_tracker"]
            ]

        # Set list of all trackers.
        self.allTrackers = self.aephirTrackers + self.kristinaTrackers + self.emilieTrackers + self.naiaTrackers

        # Run "whereAreWe" for any change in any tracker.
        for entity in any[self.allTrackers]:
            self.listen_state(whereAreWe, entity)


    def whereAreWe(self, entity, attribute, old, new, kwargs):

        # Get entity that triggers script. I don't need this, this is "entity" that's passed from "initialize", right?
        triggeredEntity = entity

        # Variables to show in frontend
        newFriendlyNam = ''
        newEntityPicture = ''
        metatrackerName = ''

        # Uncomment first time you run this to create meta device trackers in home assistant.
        # self.set_state('device_tracker.meta_walden', state='home')
        # self.set_state('device_tracker.meta_kristina', state='home')
        # self.set_state('device_tracker.meta_emilie', state='home')
        # self.set_state('device_tracker.meta_naia', state='home')

        # Set variables
        if triggeredEntity in self.aephirTrackers:
            newFriendlyName = 'Walden Meta Tracker'
            newEntityPicture = '/local/images/brain.jpg'
            metatrackerName = 'device_tracker.meta_walden'
        elif triggeredEntity in self.kristinaTrackers:
            newFriendlyName = 'Kristina Meta Tracker'
            newEntityPicture = '/local/images/kristina_3.jpg'
            metatrackerName = 'device_tracker.meta_kristina'
        elif triggeredEntity in self.emilieTrackers:
            newFriendlyName = 'Emilie Meta Tracker'
            newEntityPicture = '/local/images/emilie.jpg'
            metatrackerName = 'device_tracker.meta_emilie'
        elif triggeredEntity in self.naiaTrackers:
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
        newSource = self.get_state(triggeredEntity, attribute = 'source_type')
        newFriendlyName_temp = self.get_state(triggeredEntity, attribute = 'friendly_name')

        # If GPS source, set new coordinates
        if newSource == 'gps':
            newLatitude = self.get_state(triggeredEntity, attribute = 'latitude')
            newLongitude = self.get_state(triggeredEntity, attribute = 'longitude')
            newgpsAccuracy = self.get_state(triggeredEntity, attribute = 'gps_accuracy')

        # If not, keep last known coordinates
        elif self.get_state(metatrackerName, attribute = 'latitude') is not None:
            newLatitude = self.get_state(metatrackerName, attribute = 'latitude')
            newLongitude = self.get_state(metatrackerName, attribute = 'longitude')
            newgpsAccuracy = self.get_state(metatrackerName, attribute = 'gps_accuracy')

        # Otherwise return null
        else:
            newLatitude = None
            newLongitude = None
            newgpsAccuracy = None

        # Get battery state
        if self.get_state(triggeredEntity, attribute = 'battery') is not None:
            newBattery = self.get_state(triggeredEntity, attribute = 'battery')
        elif self.get_state(metatrackerName, attribute = 'battery') is not None:
            newBattery = self.get_state(metatrackerName, attribute = 'battery')
        else:
            newBattery = None

        # Get velocity
        if self.get_state(triggeredEntity, attribute = 'velocity') is not None:
        # if self.get_state(triggeredEntity, state = newState, attribute = 'velocity') is not None:
            newVelocity = self.get_state(triggeredEntity, attribute = 'velocity')
            # newVelocity = newState.get_state(attribute = 'velocity')
        elif self.get_state(metatrackerName, attribute = 'velocity') is not None:
        # elif self.get_state(metatrackerName, state = currentState, attribute = 'velocity') is not None:
            newVelocity = self.get_state(metatrackerName, attribute = 'velocity')
            # newVelocity = currentState.get_state(attribute = 'velocity')
        else:
            newVelocity = None

        if newState is not None:
        # if newState.state is not None:
            newStatus = newState
            # newStatus = newState.state
        else:
            newStatus = currentState
            # newStatus = currentState.state

        # Create device_tracker.meta entity
        self.set_state(metatrackerName, attributes = {
        # self.set_state(metatrackerName, state = newStatus, attributes = {
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
