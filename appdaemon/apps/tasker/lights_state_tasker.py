# Script to send the state of lights to Tasker.
# This allows the KWGT widget to change, even if the light has been toggled from elsewhere.

import appdaemon.plugins.hass.hassapi as hass
import requests

class NotifyTasker(hass.Hass):

  def initialize(self):
    self.listen_state(self.light_on,self.args["entityID"], new="on")
    self.listen_state(self.light_off,self.args["entityID"], new="off")

  def light_on (self, entity, attribute, old, new, kwargs):
    if self.args["entityID"] == "light.kitchen_lights":
      requests.get(self.args['autoremote_url'] + 'kitchen_lights_state_is=:=on')
    elif self.args["entityID"] == "light.dining_room_lights":
      requests.get(self.args['autoremote_url'] + 'dining_room_lights_state_is=:=on')
    elif self.args["entityID"] == "light.conservatory_lights":
      requests.get(self.args['autoremote_url'] + 'conservatory_lights_state_is=:=on')
    elif self.args["entityID"] == "light.bedroom":
      requests.get(self.args['autoremote_url'] + 'bedroom_lights_state_is=:=on')
    elif self.args["entityID"] == "light.baby_room":
      requests.get(self.args['autoremote_url'] + 'baby_room_lights_state_is=:=on')

  def light_off (self, entity, attribute, old, new, kwargs):
    if self.args["entityID"] == "light.kitchen_lights":
      requests.get(self.args['autoremote_url'] + 'kitchen_lights_state_is=:=off')
    elif self.args["entityID"] == "light.dining_room_lights":
      requests.get(self.args['autoremote_url'] + 'dining_room_lights_state_is=:=off')
    elif self.args["entityID"] == "light.conservatory_lights":
      requests.get(self.args['autoremote_url'] + 'conservatory_lights_state_is=:=off')
    elif self.args["entityID"] == "light.bedroom":
      requests.get(self.args['autoremote_url'] + 'bedroom_lights_state_is=:=off')
    elif self.args["entityID"] == "light.baby_room":
      requests.get(self.args['autoremote_url'] + 'baby_room_lights_state_is=:=off')
