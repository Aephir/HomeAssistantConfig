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

        lights_entity = 'https://autoremotejoaomgcd.appspot.com/sendmessage?key=APA91bHdG9gIIRophSN4rAlk4Y23LJa9o4KH_Q4I44Fzzf3luTHuOITsn0wOwZg3OhfdiPYsjYgWST8ckLapuJPjcHmY4y9G1cHOW96otuGr4M-irV57GXOHP4dC9QVNGcDOckZk2A45&message=light_entity=:=' + entity[6:]
        lights_brightness = 'https://autoremotejoaomgcd.appspot.com/sendmessage?key=APA91bHdG9gIIRophSN4rAlk4Y23LJa9o4KH_Q4I44Fzzf3luTHuOITsn0wOwZg3OhfdiPYsjYgWST8ckLapuJPjcHmY4y9G1cHOW96otuGr4M-irV57GXOHP4dC9QVNGcDOckZk2A45&message=brightness=:='

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
