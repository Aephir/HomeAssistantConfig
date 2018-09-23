import appdaemon.plugins.hass.hassapi as hass
import time

## Flash lightst (in red if available) when alarm has been triggered

class AlarmLights(hass.Hass):

  def initialize(self):
      while state.alarm_control_panel.house == "triggered":
          return light.conservatory.turn_on
          return light.XXX.turn_on
          time.sleep(1)
          return light.conservatory.turn_off
          return light.XXX.turn_off
