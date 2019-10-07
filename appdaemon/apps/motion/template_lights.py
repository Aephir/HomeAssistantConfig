"""
Motion sensors to control the main floor kitchen lights.
"""

import appdaemon.plugins.hass.hassapi as hass

# Global apps/functions to use/import. Need to figure out how!!
#   > workday_when_waking (uses workday sensor, vacaton mode sensor, pre-post midnight)
#   > cooking (uses cooking mode and time of day, both morning and evening)
#   >
#

def toInt(inString):
    try:
        return int(float(inString))
    except ValueError:
        return 0

class MotionClass(hass.Hass):

    def initialize(self):
        """ Initializes and listens for state changes in motion sensor"""

        # list of lights that are turned on by the motion.
        self.lights                 = [
            'light.kitchen_spots',
            'light.kitchen_cabinet_lights'
            ]

        # list of motion sensors that trigger the automation.
        self.motion_sensors         = [
            'binary_sensor.presence_kitchen'
            ]

        # list of illumination sensors
        self.illumination_sensors   = [
            'sensor.lightlevel_kitchen'
            ]
        
        # list of input_booleans
        self.input_booleans         = [
            'input_boolean.cooking_mode'
            ]

        self.timer = None

        for entity in self.motion_sensors:
            self.listen_state(self.motionTrigger, entity) # motion sensors

        self.listen_state(self.motionTrigger,'switch.switch')

        self.listen_state(self.inputBoolean,"input_boolean.main_floor_lights_motion_control")
        self.listen_state(self.motionTrigger,"input_boolean.cooking_mode")

    def awake(self):
        work_next_morning   = self.now_is_between("12:00:00", "00:00:00") and
            self.get_state('binary_sensor.workday_tomorrow') == 'on' or
            self.now_is_between("00:00:00", "08:00:00") and
            self.get_state('binary_sensor.workday_today') == 'on'
            
        self.get_state

    def lightsOff(self, kwargs):
        """ iterates through lights and turns them off"""
        for entity in self.light_entity_ids:
            self.turn_off(entity)
        self.cancel_timer(self.timer)

    def lightsOn(self, illumination):
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
                    self.turn_on('light.kitchen_cabinet_light_2', brightness=255, kelvin=2700)
                else:
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
            else:
                if cooking:
                    self.turn_on('light.kitchen_cabinet_lights', brightness=255, kelvin=2700)
                        # self.call_service('remote/send_command', entity_id = 'remote.kitchen_remote', command = 'fume_hood_lights')
                elif self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_cabinet_light_2', brightness=255, kelvin=2700)
        elif self.now_is_between("21:00:00", "22:00:00"):
            if dark:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
                    self.turn_on('light.kitchen_cabinet_light_2', brightness=255, kelvin=2700)
                elif any([ self.isOn(entity_id) for entity_id in ['light.dining_table_lights', 'light.conservatory_lights']]):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2700)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)
            else:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_cabinet_light_2', brightness=255, kelvin=2700)
                elif any([ self.isOn(entity_id) for entity_id in ['light.dining_table_lights', 'light.conservatory_lights']]):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2700)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)
        elif self.now_is_between("22:00:00", "07:00:00"): # everything between 22 and 7
            if dark:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_spots',brightness=255, kelvin=2700)
                    self.turn_on('light.kitchen_cabinet_light_2', brightness=255, kelvin=2700)
                elif self.isOn('light.dining_table_lights'):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2200)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)
            else:
                if self.get_state('switch.switch') == 'on':
                    self.turn_on('light.kitchen_cabinet_light_2', brightness=255, kelvin=2700)
                elif self.isOn('light.dining_table_lights'):
                    self.turn_on('light.kitchen_spots', brightness=255, kelvin=2200)
                else:
                    self.turn_on('light.kitchen_spots', brightness=10, kelvin=2200)


    def motionTrigger(self, entity, attribute, old, new, kwargs):
        """
        On motion: Turn off timer (if running), and turn on lights.
        On motion off: Start timer, turn off lights after 5 minutes.
        """

        if self.timer != None and entity != 'switch.switch':
            self.cancel_timer(self.timer)

        if self.get_state('binary_sensor.presence_kitchen') == 'on': # if we got motion.
            illumination = max([toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
            self.cancel_timer(self.timer)
            self.lightsOn(illumination)
        elif self.get_state('binary_sensor.presence_kitchen') == 'off': # we got no motion.
            self.timer = self.run_in(self.lightsOff, 90)


    def switchOff(self, entity, attribute, old, new, kwargs):
        """
        If the espresso machine is switched off and there's no motion in the kitchen, turn off lights.
        """

        if self.get_state('binary_sensor.presence_kitchen') == 'off': # we got no motion.
            self.lightsOff()


    def inputBoolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            if self.get_state("binary_sensor.presence_kitchen") == "on":
                illumination = max([ toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
                self.lightsOn(illumination)
