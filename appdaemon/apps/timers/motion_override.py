import appdaemon.plugins.hass.hassapi as hass


class Notify(hass.Hass):

    def initialize(self):

        self.top_timer = None
        self.main_timer = None
        self.basement_timer = None

        self.override_timers = [
            'input_number.override_top_floor_motion',
            'input_number.override_main_floor_motion',
            'input_number.override_basement_motion'
            ]

        self.input_booleans = [
            'input_boolean.top_floor_lights_motion_control',
            'input_boolean.main_floor_lights_motion_control',
            'input_boolean.basement_lights_motion_control'
            ]

        self.timers = [
            self.top_timer,
            self.main_timer,
            self.basement_timer
            ]

        for i in self.override_timers:
            self.listen_state(self.overrideTimer, i)

        for i in XXX:
            self.listen_state(self.cancelTimer, i)


    def overrideTimer(self, entity, attributes, old, new, kwargs):

        time = self.get_state(entity)

        boolean = self.input_booleans[self.override_timers.index(entity)]

        self.turn_off(boolean)


    def cancelTimer(self, entity):

        self.cancel_timer()
