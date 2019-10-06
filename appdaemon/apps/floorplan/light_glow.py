# Toggle dummy switches used for the light glow effect in floorplan

import appdaemon.plugins.hass.hassapi as hass

class Cosmetic(hass.Hass):

    def initialize(self):

        self.lights = [
            'light.baby_room',
            'light.bathroom',
            'light.bedroom',
            'light.basement_entrance_lights',
            'light.conservatory_couch',
            'light.conservatory_lights',
            'light.dining_table_lights',
            'light.entrance_lights',
            'light.kitchen_cabinet_lights',
            'light.kitchen_spots',
            'light.living_room_lightstrip',
            'light.stairway_down',
            'light.stairway_up',
            'light.top_floor_bathroom',
            'light.top_floor_hallway',
            'light.top_floor_tv_area',
            'light.tv_room',
            'light.walk_in_closet',
            'light.lightstrip_1'
            ]

        self.dummyLights = [
            'input_boolean.light_baby_room',
            'input_boolean.light_basement_entrance_lights',
            'input_boolean.light_bathroom',
            'input_boolean.light_bedroom',
            'input_boolean.light_conservatory_couch',
            'input_boolean.light_conservatory_lights',
            'input_boolean.light_dining_table_lights',
            'input_boolean.light_entrance_lights',
            'input_boolean.light_kitchen_cabinet',
            'input_boolean.light_kitchen_spots',
            'input_boolean.light_living_room_lightstrip',
            'input_boolean.light_stairway_down',
            'input_boolean.light_stairway_up',
            'input_boolean.light_top_floor_bathroom',
            'input_boolean.light_top_floor_hallway',
            'input_boolean.light_top_floor_tv_area',
            'input_boolean.light_tv_room',
            'input_boolean.light_walk_in_closet',
            'input_boolean.light.lightstrip_1'
            ]

        for entity in self.lights:
            self.listen_state(self.toggleDummy,entity)

        for entity in self.lights:
            state = self.get_state(entity)
            dummyID = 'input_boolean.light_' + entity[6:]
            if state == 'on':
                self.turn_on(dummyID)
            elif state == 'off':
                self.turn_off(dummyID)


    def toggleDummy(self, entity, attribute, old, new, kwargs):

        """
        Toggles the dummy input_boolean corresponding to the light switched.
        """

        dummyID = 'input_boolean.light_' + entity[6:]

        if new == 'on':
            self.turn_on(dummyID)
        elif new == 'off':
            self.turn_off(dummyID)
