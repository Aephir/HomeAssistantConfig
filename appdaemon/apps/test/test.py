# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Test(hass.Hass):

    def initialize(self):
        self.listen_state(self.testFunction, "input_boolean.guest_mode")

    def testFunction(self, entity, attribute, old, new, kwargs):
        self.log("test log entry 1")
        self.log(self.app_config['global_sensors']['motionSensors'])
        time_app = self.get_app("time_functions")
        workday = time_app.workday
        self.log(workday)



# someapp = self.get_app("SomeApp")
# some_apps_args = someapp.args

# self.app_config[all_sensors.py]['motionSensors']
# self.app_config[you main app]['sensors']
