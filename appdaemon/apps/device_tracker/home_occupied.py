# Script to track house occupancy.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class HomeOccupancy(hass.Hass):

    def initialize(self):
        self.listen(self.occupancy,"input_boolean.aephirhome360")
        self.listen(self.occupancy,"input_boolean.kristinahome360")
        self.listen(self.occupancy,"input_boolean.emiliehome360")
        self.listen(self.occupancy,"input_boolean.naiahome360")
        self.listen(self.occupancy,"input_boolean.guest_mode")


    def whereIs(self, entity_id):
        return self.get_state(entity_id)

    def occupancy(self, entity_id):
        aephir = ''
        kristina = ''
        emilie = ''
        naia = ''
        guest_mode = ''


    def 
