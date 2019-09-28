import appdaemon.plugins.hass.hassapi as hass
import requests

class NotifyTasker(hass.Hass):

  def initialize(self):
    self.listen_state(self.espresso_on,self.args["entityID"], new="on")
    self.listen_state(self.espresso_off,self.args["entityID"], new="off")

  def espresso_on (self, entity, attribute, old, new, kwargs):
    url = self.args['autoremote_url'] + '' + self.args["entityID"] + '=:=' + hass.get_state(self.args["entityID"].brightness)
    requests.get(url)

  def espresso_off (self, entity, attribute, old, new, kwargs):
    requests.get(self.args['autoremote_url'] + 'fountain_state_is=:=off')
