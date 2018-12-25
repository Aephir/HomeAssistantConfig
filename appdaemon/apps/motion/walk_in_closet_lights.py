# Toggle walk-in closet lighs based on motion

import appdaemon.plugins.hass.hassapi as hass

class MotionClass(hass.Hass):
    def initialize(self):

        # list of lights that are turned on by the motion.
        self.light_entity_ids = [
            'light.walk_in_closet'
            ]

        # list of motion sensors that trigger the automation.
        self.motion_entity_ids = [
            'binary_sensor.walk_in_closet_motion_sensor' # Walk-in closet
            ]

        # list of illumination sensors
        self.illumination_sensors = [
            'sensor.aeotec_zw100_multisensor_6_luminance'
            ]

        # create the listeners for each motion sensor.
        for entity in self.motion_entity_ids:
            self.listen_state(self.motionTrigger, entity) # motion sensors


    def motionTrigger(self, entity, attribute, old, new, kwargs):

        if self.get_state(self.args["entity_override"]) == "off":
            # this will be triggered by
            if new == 'on': # if we got motion.
                self.turn_on('light.walk_in_closet',brightness=255, kelvin=4000)
            elif new == 'off': # we got no motion.
                self.turn_off('light.walk_in_closet')
