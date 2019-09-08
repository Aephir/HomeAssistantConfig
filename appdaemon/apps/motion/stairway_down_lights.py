"""
Motion sensors to control the stairway lights going down.
"""

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

def toInt(inString):
    try:
        return int(float(inString))
    except ValueError:
        return 0

class MotionClass(hass.Hass):

    def initialize(self):
        # Motion sensors.

        self.motion_sensors = [
            "binary_sensor.motion_sensor_158d00023e3742", # Entrance Motion Sensor
            "binary_sensor.motion_sensor_158d000210ca6f" # Basement Stairway Motion Sensor
            ]

        self.illumination_sensors = [
            "sensor.illumination_158d00023e3742" # Entrance Motion Illumination Sensor
            ]

        for entity in self.motion_sensors:
            self.listen_state(self.motionTrigger,entity)
        #
        # for entity in self.illumination_sensors:
        #     self.listen_state(self.motionTrigger,entity)

        self.listen_state(self.inpuBoolean,"input_boolean.basement_lights_motion_control")


    def areWeAwake(self, entity):
        """ Check whether anyone is awake"""
        if self.get_state(entity) == "on":
            return True

    # Returns value of state as integer. Might need to remove the "float" is you get errors.
    def getIntegerState(self, entity_id):
        """ Get integer of illumination state"""
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0

    def motionTrigger(self, entity, attribute, old, new, kwargs):
        """ Turn on/off lights"""
        sensor_1_state = self.get_state("binary_sensor.motion_sensor_158d00023e3742") # Entrance Motion
        sensor_2_state = self.get_state("binary_sensor.motion_sensor_158d000210ca6f") # Basement Stairway Motion

        awake = self.areWeAwake("light.living_room_lights")
        party_mode = self.get_state('input_boolean.party_mode') == 'on'

        if sensor_2_state == "on":
            self.turn_on("light.stairway_down",brightness=255,kelvin=2700)

        elif sensor_1_state == "on" and sensor_2_state == "off":
            if party_mode:
                self.turn_on("light.stairway_down",brightness=255,kelvin=2700)
                
            elif self.now_is_between('07:00:00', '22:00:00'):

                self.turn_on("light.stairway_down",brightness=255,kelvin=2700)

            elif self.now_is_between('22:00:00', '07:00:00'):
                if awake:
                    self.turn_on("light.stairway_down",brightness=255,kelvin=2200)
                else:
                    self.turn_on("light.stairway_down",brightness=10,kelvin=2200)

        elif sensor_1_state == "on" and sensor_2_state == "on":
            self.turn_on("light.stairway_down",brightness=255,kelvin=2700)

        else:
            self.turn_off("light.stairway_down")

    def inpuBoolean(self, entity, attribute, old, new, kwargs):

        if new == "on":
            self.motionTrigger(entity, attribute, old, new, kwargs)
