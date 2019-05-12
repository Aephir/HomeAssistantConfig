"""
Script to turn on/off lights to make it look like someone is home.
"""

import appdaemon.plugins.hass.hassapi as hass
import datetime

class AwayLights(hass.Hass):

    def initialize(self):

        self.vacationMode = [
            'input_boolean.vacation_mode'
            ]

        self.deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        self.kitchen_lights = [
            'light.kitchen_spots'
            ]

        self.dining_room_lights = [
            'light.dining_table_lights'
            ]

        self.conservatory_lights    = [
            'light.conservatory_lights'
            ]

        self.top_floor_lights   = [
            'light.top_floor_hallway',
            'light.top_floor_tv_area'
            ]

        self.basement_lights    = [
            'light.tv_room'
            ]

        self.lights = [
            self.kitchen_lights,
            self.dining_room_lights,
            self.conservatory_lights,
            self.top_floor_lights,
            self.basement_lights
            ]

        self.handle = self.run_at_sunset(self.homeAloneLights, offset=300)

        # for device in self.deviceTrackers:
        #     self.listen_state(self.homeAloneLights, device)

        for entity in self.vacationMode:
            self.listen_state(self.homeAloneLights, entity, new = 'on')


    def someoneHome(self):
        home = 0
        for i in deviceTrackers:
            if self.get_state(i) == home:
                home += 1
        if home > 0:
            return True
        else:
            return False

    def homeAloneLights(self, entity, attribute, old, new, kwargs):
        """
        Get time as time of day
        Use run_in with random_start or random_end
        """


        testTime = '2018-12-24 15:29:41.893370'
        cookingTime = '2018-12-24 16:08:41.893370'
        diningTime = '2018-12-24 18:10:46.893370'
        hyggeTime = '2018-12-24 19:31:11.893370'
        eveningTime = '2018-12-24 20:01:56.893370'
        bedTime = '2018-12-24 23:34:41.893370'
        lightsOut = '2018-12-25 01:12:41.893370'

        if self.get_state('sun.sun') == 'below_horizon' and self.someoneHome() == False and self.get_state('input_boolean.vacation_mode') == 'on':

            self.handle = self.run_at(self.lightsCooking, cookingTime)
            self.handle = self.run_at(self.lightsDining, diningTime)
            self.handle = self.run_at(self.lightsHygge, hyggeTime)
            self.handle = self.run_at(self.lightsEvening, eveningTime)
            self.handle = self.run_at(self.lightsBedtime, bedTime)
            self.handle = self.run_at(self.lightsOut, lightsOut)

            self.handle = self.run_at(self.lightsTest, testTime)

        self.handle = self.run_in(callback, 120, random_start = -60, **kwargs)


    def lightsTest(self, entity, attribute, old, new, kwargs):
        self.lights_on('light.bedroom')
        self.lights_on('light.baby_room')
        self.lights_on('light.bathroom')

    # def lightsTest(self, entity, attribute, old, new, kwargs):
    #     self.lights_on('light.kitchen_lights')
    #     self.lights_on('light.dining_room_lights')
    #     self.lights_on('light.top_floor_hallway')


    def lightsCooking(self, entity, attribute, old, new, kwargs):
        for light in self.kitchen_lights:
            self.lights_on(light)


    def lightsDining(self, entity, attribute, old, new, kwargs):
        for light in self.dining_room_lights:
            self.lights_on(light)
        for light in self.kitchen_lights:
            self.lights_off(light)


    def lightsHygge(self, entity, attribute, old, new, kwargs):
        for light in self.dining_room_lights:
            self.lights_on(light)
        for light in self.conservatory_lights:
            self.lights_on(light)
        for light in self.kitchen_lights:
            self.lights_off(light)

    def lightsEvening(self, entity, attribute, old, new, kwargs):
        self.lights_off('light.top_floor_hallway')
        self.lights_on('light.bedroom')
        for light in self.top_floor_lights:
            self.lights_on(light)

    def lightsBedtime(self, entity, attribute, old, new, kwargs):
        self.lights_off('light.dining_room_lights')

    def lightsBedtime(self, entity, attribute, old, new, kwargs):
        self.lights_off('light.top_floor_hallway')
        self.lights_off('light.kitchen_lights')
        self.lights_off('light.dining_room_lights')
        self.lights_off('light.bedroom')
        self.lights_off('light.conservatory_lights')
        self.lights_off('light.top_floor_hallway')
        self.lights_off('light.top_floor_hallway')
        self.lights_off('light.bathroom')
