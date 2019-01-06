# Toggle dummy switches used for the light glow effect in floorplan

import appdaemon.plugins.hass.hassapi as hass

class Cosmetic(hass.Hass):

    def initialize(self):

        self.lights = [
            '',
            ]

        self.dummyLights = [
            '',
            ]

        for light in self.lights:
            self.listen_state(toggleDummy,light)

    def toggleDummy(self, entity, attribute, old, new, kwargs):

        dummy_id = 'input_boolean.light_' + entity[5:]

        if new == 'on':
            self.turn_on(dummy_id)

        elif new == ' off':
            self.turn_off(dummy_id)

        # for self.lights[x]:
        #     self.toggle(self.dummyLights[x])
