import hassapi as hass

class Lights(hass.Hass):

    def initialize(self):

        self.listen_state(self.toggle_lights, 'sun.sun')

    def toggle_lights(self, entity, attribute, old, new, kwargs):

        if new == 'above_horizon':
            self.turn_on('switch.shed_switch_1')
        elif new == 'below_horizon':
            self.turn_off('switch.shed_switch_1')
