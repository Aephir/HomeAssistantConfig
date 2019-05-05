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

        # list of lights that are turned on by the motion.
        self.motion_sensors = [
            'binary_sensor.motion_sensor_158d000210ca6e', # Bathroom #1 sensor
            'binary_sensor.motion_sensor_158d000236a22f' # Bathroom #2 sensor
            ]

        # list of illumination sensors
        self.illumination_sensors = [
            'sensor.illumination_158d000236a22f'
            ]

        self.light_entity_ids = [
            'light.bathroom'
            ]

        for entity in self.motion_sensors:
            self.listen_state(self.motionTrigger, entity)

        for entity in self.illumination_sensors:
            self.listen_state(self.motionTrigger, entity)

        self.listen_state(self.inpuBoolean,"input_boolean.bathroom_lights_motion_control")


    # Returns True/False based on state of entity (assess whether we are awake). Find better proxy eventually.
    def areWeAwake(self, entity):
        """ Check whether anyone is awake"""
        if self.get_state(entity) == "on":
            return True

    # Returns value of state as integer. Might need to remove the "float" is you get errors.
    def getIntegerState(self, entity_id):
        """ Get integer of illumination state"""
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0

    def isOn(self, entity_id):
        """ Check whether an entity_id state is 'on'"""
        return self.get_state(entity_id) == 'on'

    def lightsOff(self):
        """ iterates through lights and turns them off"""
        for entity in self.light_entity_ids:
            self.turn_off(entity)


    def lightsOn(self, illumination):
        """ Turns the lights on, depending on time and awake state"""

        awake = self.areWeAwake('light.dining_room_lights')

        if self.now_is_between("07:00:00", "21:00:00") and illumination < 50:
            self.turn_on('light.bathroom', brightness=255, kelvin=2700)
        elif self.now_is_between("21:00:00", "22:00:00") and illumination < 50:
            if awake:
                self.turn_on('light.bathroom', brightness=255, kelvin=2700)
            else:
                self.turn_on('light.bathroom', brightness=150, kelvin=2200)
        elif self.now_is_between("22:00:00", "07:00:00"): # everything between 22 and 7
            if awake:
                self.turn_on('light.bathroom', brightness=255, kelvin=2200)
            else:
                self.turn_on('light.bathroom', brightness=10, rgb_color=[255,0,0])


    def motionTrigger(self, entity, attribute, old, new, kwargs):
        """
        Passes the maximum illumination from any sensor on the list, and passes to lightsOn upon motion.
        Turns off light when motion stops
        """
        if new == 'on':
            illumination = max([ toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
            self.lightsOn(illumination)
        elif new == 'off': # we got no motion.
            if self.get_state('binary_sensor.motion_sensor_158d000210ca6e') == 'off' and self.get_state('binary_sensor.motion_sensor_158d000236a22f') == 'off':
                self.lightsOff()

    def inpuBoolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            if self.get_state("binary_sensor.motion_sensor_158d0001e0a8e1") == "on":
                illumination = max([ toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
                self.lightsOn(illumination)
