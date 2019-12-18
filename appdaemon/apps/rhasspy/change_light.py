# import hassapi as hass
import appdaemon.plugins.hass.hassapi as hass

class Rhasspy(hass.Hass):

    def initialize(self):

        self.light      = {

            "baby room lights":"light.baby_room_lights",
            "basement":"light.basement_lights",
            "bathroom":"light.bathroom",
            "bedroom lights":"light.bedroom",
            "changing table":"light.changing_table",
            "conservatory couch":"light.conservatory_couch",
            "conservatory floor":"light.conservatory_floor_1",
            "conservatory lights":"light.conservatory_lights",
            "dining room":"light.dining_room_lights",
            "dining table":"light.dining_table_lights",
            "entrance":"light.entrance_lights",
            "kitchen cabinets":"light.kitchen_cabinet_lights",
            "kitchen":"light.kitchen_lights",
            "kitchen spots":"light.kitchen_spots",
            "xxxxxxxx":"light.lightstrip_1",
            "living room lightstrip":"light.living_room_lightstrip",
            "main floor":"light.main_floor_lights",
            "upstairs hallway":"light.top_floor_hallway",
            "upstairs":"light.top_floor_lights",
            "upstairs living room":"light.top_floor_tv_area",
            "TV room":"light.tv_room_lights"
        }

        if 'event' in self.args:
            self.listen_event(self.change_light, self.args['event'])

    def change_light(self, event_name, data, kwargs):

        self.log("Rhasspy")

        light           = data['name']
        # color           =
        try:
            brightness  = data['brightness']
        except:
            brightness      = 255
        state           = data['state']

        if state == 'on':
            self.turn_on(self.light[light]) # Add variables, brightness, color, (effect?)
        elif state == 'on':
            self.turn_off(self.light[light])
