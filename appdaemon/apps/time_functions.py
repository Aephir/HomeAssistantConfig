# List of all relevant sensors
# Use in another app by:
# self.app_config[you main app]['sensors']. For this app (all_sensors.py):
# self.app_config[all_sensors.py]['motionSensors']

# Ok there are 2 main ways to approach this, which I can suggest.
# Have the main app, in which in its config you have all your sensors, and give it a lower priority than 50; say 40. In the app, have it that when it starts up, it reads its self.args where you have the sensors, and it loads into the self.global_vars variable, so other apps can pick it up from there
# also ensure this app, is a dependent to other apps, so when you change the sensors, the others reload and get the new update
# another way to so it, is if you want to avoid loading into another variable, or avoid writing more code, all you can so is in the other apps, call self.app_config[you main app]['sensors']
# The others will always get the latest update
# Ensure in the main app config, they are put in there as a list or something

import appdaemon.plugins.hass.hassapi as hass

class GlobalFunctions(hass.Hass):

    def initialize(self):
        self.listen_state(self.test,'input_boolean.vacation_mode')

    def test(self, entity, attribute, old, new, kwargs):
        self.log("new test from root dir")
        new = self.GlobalFunctions.testFunction()
        self.log(str(new))
