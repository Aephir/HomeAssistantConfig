# Motion sensors to control the main floor bathroom lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):
        # Motion detected = lights on; motion stops = lights off.
        self.listen_state(self.switchonoff,"binary_sensor.motion_sensor_158d000210ca6e") # Bathroom #1 sensor
        self.listen_state(self.switchonoff,"binary_sensor.motion_sensor_158d000236a22f") # Bathroom #2 sensor
        # Illumination drops while motion sensor is "on" = light on.
        self.listen_state(self.switchonoff,"sensor.illumination_158d000236a22f")

    # Returns True/False based on state of entity (assess whether we are awake). Find better proxy eventually.
    def areWeAwake(self, entity):
        if self.get_state(entity) == "on":
            return True

    # Return True/False for whether entity_id has state "on".
    def isOn(self, entity_id):
        return self.get_state(entity_id) == 'on'

    # Returns value of state as integer. Might need to remove the "float" is you get errors.
    def getIntegerState(self, entity_id):
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0

    # If motion sensor_1 detects motion, and turn on light
    # (if day and light levels are low, or turn on dim/red if night and we are not awake).
    def switchonoff(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state("binary_sensor.motion_sensor_158d000210ca6e")
        sensor_2_state = self.get_state("binary_sensor.motion_sensor_158d000236a22f")
        illumination_2 = self.getIntegerState("sensor.illumination_158d000236a22f")

        if sensor_1_state == "on" or sensor_2_state == "on":
            if self.now_is_between("07:00:00", "21:00:00"):
                if illumination_2 < 50:
                    self.turn_on("light.bathroom",brightness=255,kelvin=2700)

            elif self.now_is_between("21:00:00", "22:00:00"):
                if illumination_2 < 50:
                    if self.areWeAwake("light.dining_table_lights") == True or self.areWeAwake("light.conservatory_lights") == True:
                        self.turn_on("light.bathroom",brightness=255,kelvin=2200)
                    else:
                        self.turn_on("light.bathroom",brightness=10,rgb_color=[255,0,0])

            elif self.now_is_between("22:00:00", "07:00:00"):
                if self.areWeAwake("light.dining_table_lights") == True:
                    self.turn_on("light.bathroom",brightness=255,kelvin=2200)
                else:
                    self.turn_on("light.bathroom",brightness=10,rgb_color=[255,0,0])

        else:
            self.turn_off("light.bathroom")
