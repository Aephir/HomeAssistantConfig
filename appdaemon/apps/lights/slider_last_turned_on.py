'''
Light brightness slider
for KWGT widget
'''

import appdaemon.plugins.hass.hassapi as hass
import datetime

class LightSlider(hass.Hass):

    def initialize(self):

        self.lights = [
            'light.kitchen_lights',
            'light.dining_room_lights',
            'light.conservatory_lights',
            'light.bedroom',
            'light.baby_room',
            'light.wine_cellar'
            ]

        self.input = [

            ]

        self.last_turned_on = ''

        for entity in self.lights:
            self.listen_state(lightSliderReport,entity)


    def lightSliderReport(self, entity, attribute, old, new, kwargs):

        lights_entity = self.args['autoremote_url'] + 'light_entity=:=' + entity[6:]
        lights_brightness = self.args['autoremote_url'] + 'brightness=:='

        if new == 'on':
            lights_brightness += brightness
        else:
            lights_brightness += '0'

        requests.get(lights_entity)
        requests.get(lights_brightness)


    def lightSliderInputIncrease(self, entity, attribute, old, new, kwargs):

        light =
        brightness = int(self.get_state(light, attribute='brightness')) + 25

        self.turn_on(light, brightness = brightness)

    def lightSliderInputDecrease(self, entity, attribute, old, new, kwargs):

        light =
        brightness = int(self.get_state(light, attribute='brightness')) - 25

        self.turn_on(light, brightness = brightness)
