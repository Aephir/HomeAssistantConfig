# Heating control

import appdaemon.plugins.hass.hassapi as hass


class HeatingAutomations(hass.Hass):

    def initialize(self):

        self.deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        self.motionSensors = [
            "sensor.illumination_158d00023e3742",
            "binary_sensor.motion_sensor_158d000200d285"
            ]

        self.arrived_home = None

        for entity in self.deviceTrackers:
            self.listen_state(self.arrivedHome, entity, new="home")

        self.listen_state(self.motionDining, "sensor.illumination_158d00023e3742", new="on")
        self.listen_state(self.motionConservatory, "binary_sensor.motion_sensor_158d000200d285", new="on")


    def arrivedHome(self, entity, attribute, old, new, kwargs):

        if (entity == "device_tracker.meta_walden" and self.get_state("device_tracker.meta_kristina") != "home") or (entity == "device_tracker.meta_kristina" and self.get_state("device_tracker.meta_walden") != "home"):
            self.arrived_home = True
            self.run_in(timerArrived, 600)

    def timerArrived(self):
        self.arrived_home = False

    def motionDining(self, entity, attribute, old, new, kwargs):

        if self.arrived_home:
            if self.now_is_between('07:00:00', '01:00:00'):
                if self.now_is_between('07:00:00', '01:00:00'):
                    self.turn_on("light.dining_room_lights",brightness=255,kelvin=2700)
            else:
                self.turn_on("light.dining_room_lights",brightness=100,kelvin=2700)

    def motionConservatory(self, entity, attribute, old, new, kwargs):

        if self.arrived_home:
            if self.now_is_between('07:00:00', '01:00:00'):
                if self.now_is_between('07:00:00', '01:00:00'):
                    self.turn_on("light.conservatory_lights",brightness=255,kelvin=2700)
            else:
                self.turn_on("light.conservatory_lights",brightness=100,kelvin=2700)
