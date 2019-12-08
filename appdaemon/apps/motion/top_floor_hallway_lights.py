# Motion sensors to control the top floor hallway lights.

import appdaemon.plugins.hass.hassapi as hass


class MotionClass(hass.Hass):

    def initialize(self):

        self.motion_sensors = [
            'binary_sensor.presence_top_floor_stairway',    # Top floor stairway
            'binary_sensor.presence_top_floor_tv_room'      # Top floor tv room
            ]

        self.illumination_sensors   = [
            'sensor.lightlevel_top_floor_stairway'
            ]

        self.lights         = [
            'light.top_floor_hallway'
            ]

        for entity in self.motion_sensors:
            self.listen_state(self.motion_trigger,entity)

        self.timer = None # Set timer off to also reset if otther motion sensor is turned on?

        self.listen_state(self.input_boolean,"input_boolean.top_floor_lights_motion_control")


    def get_integer_state(self, entity_id):
        try:
            return int(self.get_state(entity_id))
        except ValueError:
            return 0

    def motion_trigger(self, entity, attribute, old, new, kwargs):
        """
        On motion: Turn off timer (if running), and turn on lights.
        On motion off: Start timer, turn off lights after 5 minutes.
        """

        party_mode = self.get_state('input_boolean.party_mode') == 'on'

        # if self.get_state('input_boolean.creative_lights_motion_control') == 'on':
        if party_mode:
            self.cancel_timer(self.timer)
            self.turn_on(light, brightness=255,kelvin=2700)
        elif new == 'on' and entity in self.motion_sensors:
            illumination = max([self.get_integer_state(entity_id) for entity_id in self.illumination_sensors])
            self.cancel_timer(self.timer)
            if illumination < 500:
                for light in self.lights:
                    if self.get_state(light) == 'off': # If more, use for i in self.lights:  self.turn_on(i)
                        self.lights_on(light)
        elif new == 'off' and entity in self.motion_sensors:
            if all([self.get_state(entity_id) == 'off' for entity_id in self.motion_sensors]):
                self.timer = self.run_in(self.lights_off, 3)


    def lights_on(self, light):

        if self.get_state('sensor.awake') == 'on':
            self.turn_on(light, brightness=255,kelvin=2700)
        else:
            self.turn_on(light, brightness=50,kelvin=2200)


    def lights_off(self, kwargs):

        for light in self.lights:
            self.turn_off(light)


    def input_boolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            self.motion_trigger(entity, attribute, old, new, kwargs)
