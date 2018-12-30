# Toggle walk-in closet lighs based on motion

import appdaemon.plugins.hass.hassapi as hass

class MotionClass(hass.Hass):

    def initialize(self):

        self.listen_state(self.motionTrigger, 'binary_sensor.walk_in_closet_motion_sensor')


    def motionTrigger(self, entity, attribute, old, new, kwargs):

        if new == 'on': # if we got motion.
            self.turn_on('light.walk_in_closet',brightness=255, kelvin=2700)
        elif new == 'off': # we got no motion.
            self.turn_off('light.walk_in_closet')
