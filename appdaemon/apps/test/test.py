# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Test(hass.Hass):

    def initialize(self):
        self.listen_state(self.testFunction, "input_boolean.guest_mode")

    def testFunction(self, entity, attribute, old, new, kwargs):
        self.log("test log entry")
        # entityIds = self.app_config["all_sensors"]["motionSensors"]
        entityIds = self.global_vars["all_sensors"]["motionSensors"]
        for entity in entityIds:
            self.log(entity)

# self.app_config[all_sensors.py]['motionSensors']
