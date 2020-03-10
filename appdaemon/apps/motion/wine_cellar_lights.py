"""
Motion sensors to control the wine cellar lights.
"""

import appdaemon.plugins.hass.hassapi as hass

def get_integer(string_in):
    try:
        return int(float(string_in))
    except ValueError:
        return 0

class MotionClass(hass.Hass):

    def initialize(self):
        """ Initializes and listens for state changes in motion sensor"""

        # list of lights that are turned on by the motion.
        self.light_entity_ids = [
            'light.lightstrip_1'
            ]

        # list of motion sensors that trigger the automation.
        self.motion_entity_ids = [
            'binary_sensor.presence_wine_cellar'
            ]

        self.timer = None

        for entity in self.motion_entity_ids:
            self.listen_state(self.motion_trigger, entity) # motion sensors

        self.listen_state(self.input_boolean,"input_boolean.basement_lights_motion_control")

    def lights_off(self, kwargs):
        """ iterates through lights and turns them off"""
        for light in self.light_entity_ids:
            self.turn_off(light)
        self.cancel_timer(self.timer)

    def lights_on(self):
        """ Turns the lights on, depending on time and awake state"""

        if self.now_is_between("09:00:00", "23:00:00"):
            for light in self.light_entity_ids:
                self.turn_on(light, brightness=255, kelvin=2700)
        else:
            for light in self.light_entity_ids:
                self.turn_on(light, brightness=255, kelvin=2200)

    def motion_trigger(self, entity, attribute, old, new, kwargs):
        """
        On motion: Turn off timer (if running), and turn on lights.
        On motion off: Start timer, turn off lights after 5 minutes.
        """

        if self.timer != None:
            self.cancel_timer(self.timer)

        if self.get_state('binary_sensor.presence_wine_cellar') == 'on': # if we got motion.
            self.cancel_timer(self.timer)
            self.lights_on()
        elif self.get_state('binary_sensor.presence_wine_cellar') == 'off': # we got no motion.
            self.cancel_timer(self.timer)
            self.timer = self.run_in(self.lights_off, 90)

    def input_boolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            # if any([state == 'on' for state in self.motion_entity_ids]):
            if self.get_state("binary_sensor.presence_kitchen") == "on":
                self.lights_on()