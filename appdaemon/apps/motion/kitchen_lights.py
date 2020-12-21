"""
Motion sensors to control the main floor kitchen lights.
"""

from random import randint
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
            'binary_sensor.presence_kitchen'
            ]

        # list of illumination sensors
        self.illumination_sensors = [
            'sensor.lightlevel_kitchen'
            ]

        self.timer = None

        for entity in self.motion_entity_ids:
            self.listen_state(self.motion_trigger, entity) # motion sensors

        self.listen_state(self.switch_toggle,'switch.switch')

        self.listen_state(self.input_boolean,"input_boolean.main_floor_lights_motion_control")
        self.listen_state(self.motion_trigger,"input_boolean.cooking_mode")

    def cooking(self, **kwargs):
        """ Check if we are likely to be cooking"""
        if self.get_state("input_boolean.cooking_mode") == 'on' or self.now_is_between("16:00:00", "19:00:00") or self.now_is_between("06:45:00", "08:00:00"):
            return True
        else:
            return False

    def is_on(self, entity_id):
        """ Check whether an entity_id state is 'on'"""
        return self.get_state(entity_id) == 'on'

    def lights_off(self, kwargs):
        """ iterates through lights and turns them off"""
        for entity in self.light_entity_ids:
            self.turn_off(entity)
        self.cancel_timer(self.timer)

    def lights_on(self, illumination):
        """ Turns the lights on, depending on time and awake state"""

        cooking = self.cooking()
        dark = int(illumination) < 80 # 40?? 50??
        party_mode = self.get_state('input_boolean.party_mode') == 'on'

        if party_mode:
            self.turn_on("light.kitchen_lights",brightness=255,kelvin=2700)

        elif self.now_is_between("07:00:00", "21:00:00"):
            if dark:
                if cooking:
                    for entity in self.light_entity_ids:
                        self.turn_on(entity, brightness=255, kelvin=2700)
                        # self.call_service('remote/send_command', entity_id = 'remote.kitchen_remote', command = 'fume_hood_lights')
                elif self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
                    self.turn_on('light.kitchen_cabinet_2', brightness=255, kelvin=2700)
                else:
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
            else:
                if cooking:
                    self.turn_on('light.kitchen_cabinet_lights', brightness=255, kelvin=2700)
                        # self.call_service('remote/send_command', entity_id = 'remote.kitchen_remote', command = 'fume_hood_lights')
                elif self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_cabinet_2', brightness=255, kelvin=2700)
        elif self.now_is_between("21:00:00", "22:00:00"):
            if dark:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
                    self.turn_on('light.kitchen_cabinet_2', brightness=255, kelvin=2700)
                elif any([ self.is_on(entity_id) for entity_id in ['light.dining_table_lights', 'light.conservatory_lights']]):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2700)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)
            else:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_cabinet_2', brightness=255, kelvin=2700)
                elif any([ self.is_on(entity_id) for entity_id in ['light.dining_table_lights', 'light.conservatory_lights']]):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2700)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)
        elif self.now_is_between("22:00:00", "07:00:00"): # everything between 22 and 7
            if dark:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
                    self.turn_on('light.kitchen_cabinet_2', brightness=255, kelvin=2700)
                elif self.is_on('light.dining_table_lights'):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2200)
                else:
                    light = 'light.kitchen_spot_' + str(randint(1,6))
                    self.turn_on(light, brightness=10, kelvin=2200)
            else:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_cabinet_2', brightness=255, kelvin=2700)
                elif self.is_on('light.dining_table_lights'):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2200)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)


    def motion_trigger(self, entity, attribute, old, new, kwargs):
        """
        On motion: Turn off timer (if running), and turn on lights.
        On motion off: Start timer, turn off lights after 5 minutes.
        """

        if self.timer != None:
            self.cancel_timer(self.timer)

        if self.get_state('binary_sensor.presence_kitchen') == 'on': # if we got motion.
            illumination = max([get_integer(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
            self.cancel_timer(self.timer)
            self.lights_on(illumination)
        elif self.get_state('binary_sensor.presence_kitchen') == 'off': # we got no motion.
            self.cancel_timer(self.timer)
            self.timer = self.run_in(self.lights_off, 90)


    def switch_toggle(self, entity, attribute, old, new, kwargs):
        """
        If the espresso machine is switched off and there's no motion in the kitchen, turn off lights.
        """

        if new == 'off':
            if self.get_state('light.kitchen_cabinet_1') == 'off': # cabinet light 1 is off.
                self.turn_off('light.kitchen_cabinet_2')
        elif new == 'on':
            if self.get_state('light.kitchen_spots') == 'on':
                if self.get_state('light.kitchen_cabinet_2') == 'off':
                    self.turn_on('light.kitchen_cabinet_2')


    def input_boolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            if self.get_state("binary_sensor.presence_kitchen") == "on":
                illumination = max([ get_integer(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
                self.lights_on(illumination)
