

import appdaemon.plugins.hass.hassapi as hass
import datetime

class LightSlider(hass.Hass):

    def initialize(self):

        self.last_turned_on = ''


    def
