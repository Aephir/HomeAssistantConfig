"""
Motion sensors to control the main floor bathroom lights.
"""

import appdaemon.plugins.hass.hassapi as hass

def toInt(inString):
    try:
        return int(float(inString))
    except ValueError:
        return 0

class MotionClass(hass.Hass):

    def initialize(self):
        """ Initializes and listens for state changes in motion sensor"""

        self.timer = None

        # list of lights that are turned on by the motion.
        self.light_entity_ids = [
            'light.kitchen_spots',
            'light.kitchen_cabinet_lights'
            ]

        # List of entities to assess if we are awake.
        self.awake_entity_ids = [
            'light.dining_table_lights',
            'light.conservatory_lights'
            ]

        # list of motion sensors that trigger the automation.
        self.motion_entity_ids = [
            'binary_sensor.motion_sensor_158d0001e0a8e1'
            ]

        # list of illumination sensors
        self.illumination_sensors = [
            'sensor.illumination_158d0001e0a8e1'
            ]

        for entity in self.motion_entity_ids:
            self.listen_state(self.motionTrigger, entity) # motion sensors
            # self.listen_state(self.motionTrigger, entity, new = 'on') # motion sensors

        # for entity in self.motion_entity_ids:
        #     self.listen_state(self.motionTrigger, entity, new = 'off', duration=240) # motion sensors

        self.timer = None

    def cooking(self, **kwargs):
        """ Check if we are likely to be cooking"""
        if self.get_state("input_boolean.cooking_mode") == 'on' or self.now_is_between("16:00:00", "19:00:00"):
            return True

    def isOn(self, entity_id):
        """ Check whether an entity_id state is 'on'"""
        return self.get_state(entity_id) == 'on'

    def lightsOff(self):
        """ iterates through lights and turns them off"""
        for entity in self.light_entity_ids:
            self.turn_off(entity)

    def lightsOn(self, illumination):
        """ Turns the lights on, depending on time and awake state"""

        cooking = self.cooking()

        if self.now_is_between("07:00:00", "21:00:00") and illumination < 150:
            if cooking:
                for entity in self.light_entity_ids:
                    self.turn_on(entity, brightness=255, kelvin=2700)
                    # self.call_service('remote/send_command', entity_id = 'remote.kitchen_remote', command = 'fume_hood_lights')
            else:
                self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
        elif self.now_is_between("21:00:00", "22:00:00") and illumination < 150:
            if any([ self.isOn(entity_id) for entity_id in ['light.dining_table_lights', 'light.conservatory_lights']]):
                self.turn_on('light.kitchen_spots', brightness=255, kelvin=2700)
            else:
                self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)
        elif self.now_is_between("22:00:00", "07:00:00"): # everything between 22 and 7
            if self.isOn('light.dining_table_lights'):
                self.turn_on('light.kitchen_spots', brightness=255, kelvin=2200)
            else:
                self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)

    def motionTrigger(self, entity, attribute, old, new, kwargs):
        """
        On motion: Turn off timer (if running), and turn on lights.
        On motion off: Start timer, turn off lights after 5 minutes.
        """
        cooking = self.cooking()

        # this will be triggered by
        if new == 'on': # if we got motion.
            # if self.timer != None:
            #     self.cancel_timer(self.timer)
            # get illumination from our illumination sensors.
            illumination = max([ toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
            # turn on our lights depending on the time of day.
            self.lightsOn(illumination)
        elif new == 'off': # we got no motion.
            # self.timer = self.run_in(self.lightsOff(), 300)
            self.lightsOff()
