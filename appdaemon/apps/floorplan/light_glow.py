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

    def toggleDummy:

        for self.lights[x]:
            self.toggle(self.dummyLights[x])
