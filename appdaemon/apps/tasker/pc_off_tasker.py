# Send to tasker on Nexus 9

import appdaemon.plugins.hass.hassapi as hass
import requests

class NotifyTasker(hass.Hass):

  def initialize(self):
    self.listen_event(self.shedPCOff, "MODE_CHANGE", mode="pc_off")

  def shedPCOff(self, entity, attribute, old, new, kwargs):
    requests.get(self.args['autoremote_url'] + 'turn_shed_pc=:=off')
    self.log("PC off")
