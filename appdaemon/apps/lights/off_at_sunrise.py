import appdaemon.plugins.hass.hassapi as hass
import datetime

class Sunrise(hass.Hass):

    def initialize(self):

        self.listen_state(self.lights_off, 'sun.sun', new = 'above_horizon')

    def lights_off(self, entity, attribute, old, new, kwargs):

        lights_to_kill  = self.args['non_presence_lights']

        if self.get_state('input_boolean.basement_lights_motion_control') == 'off':
            lights_to_kill.append('light.basement_lights')
        if self.get_state('input_boolean.main_floor_lights_motion_control') == 'off':
            lights_to_kill.append('light.main_floor_lights')
        if self.get_state('input_boolean.top_floor_lights_motion_control') == 'off':
            lights_to_kill.append('light.top_floor_lights')

        for light in lights_to_kill:
            self.turn_off(light)
