# Send command to Nexus 9
# Launch app

import appdaemon.plugins.hass.hassapi as hass
import requests

class NotifyTasker(hass.Hass):

  def initialize(self):
    self.listen_state(self.launch_app,self.args["entityID"])

  def launch_app (self, entity, attribute, old, new, kwargs):
    requests.get(self.args['autoremote_url'] + 'launch_app=:=' + self.args["APP"])
