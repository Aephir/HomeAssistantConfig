import appdaemon.plugins.hass.hassapi as hass
import requests

# listen for what is sent from the "increase/decrease brightness" KWGT button (through Tasker).
# Determine the last light taht was turned on.
# Increase the brightness of that light by 10. Or 10%?

class LightBrightness(hass.Hass):

    def initialize(self):
        self.listen_state(self.which_light_up,self.args["entityID"], new="on")
        self.listen_state(self.which_light_down,self.args["entityID"], new="off")

    def which_light_up (self, entity, attribute, old, new, kwargs):
        if {%- if (as_timestamp(now()) - as_timestamp(states.light.kitchen_lights.last_changed)) < (as_timestamp(now()) - as_timestamp(states.dining_room_lights.last_changed)) and (as_timestamp(now()) - as_timestamp(states.light.kitchen_lights.last_changed)) > (as_timestamp(now()) - as_timestamp(states.light.conservatory_lights.last_changed)) and (as_timestamp(now()) - as_timestamp(states.light.kitchen_lights.last_changed)) < (as_timestamp(now()) - as_timestamp(states.light.bedroom.last_changed)) and (as_timestamp(now()) - as_timestamp(states.light.kitchen_lights.last_changed)) < (as_timestamp(now()) - as_timestamp(states.baby_room.last_changed)) and (as_timestamp(now()) - as_timestamp(states.light.kitchen_lights.last_changed)) < (as_timestamp(now()) - as_timestamp(states.entrance_lights.last_changed)) and (states.light.kitchen_lights == 'on') -%}:
            brightness: '{{states.light.kitchen_lights.attributes.brightness + 10}}'



    state = self.get_state("light.office_1", attribute = "brightness")
