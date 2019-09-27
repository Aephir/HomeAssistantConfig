# Motion sensors to control the entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):
        # Motion sensors.

        self.motionSensors = [
            "binary_sensor.motion_sensor_158d00023e3742", # Entrance Motion Sensor
            "binary_sensor.motion_sensor_158d000200e0c5", # Top Floor Stairs Motion Sensor
            "binary_sensor.motion_sensor_158d000210ca6f" # Basement Stairway Motion Sensor
            ]

        self.doorSensors = [
            "binary_sensor.door_window_sensor_158d00022d0917" # Front door
            ]

        self.illuminationSensors = [
            "sensor.illumination_158d00023e3742" # Entrance Motion Illumination Sensor
            ]

        for entity in self.motionSensors:
            self.listen_state(self.switchonoff,entity)

        for entity in self.doorSensors:
            self.listen_state(self.switchonoff,entity)

        for entity in self.illuminationSensors:
            self.listen_state(self.switchonoff,entity)

    # Assess whether we are awake, based on state of entity. Find better proxy eventually.
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

# Motion sensor lights
    def switchonoff(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state("binary_sensor.motion_sensor_158d00023e3742") # Entrance Motion
        sensor_2_state = self.get_state("binary_sensor.motion_sensor_158d000210ca6f") # Basement Stairway Motion
        sensor_3_state = self.get_state("binary_sensor.motion_sensor_158d000236a0f3") # Top Floor Stairs Motion Sensor
        sensor_4_state = self.get_state("binary_sensor.door_window_sensor_158d00022d0917") # Front door sensor
        awake = self.areWeAwake("light.living_room_lights")
        party_mode      = self.get_state('input_boolean.party_mode') == 'on'

        if sensor_1_state == "on" or sensor_2_state == "on" or sensor_3_state == "on":
            if party_mode:
                self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)
            elif self.now_is_between('07:00:00', '22:00:00'):
                # if self.getIntegerState("sensor.illumination_158d00023e3742") < 50:
                self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)

            elif self.now_is_between('22:00:00', '07:00:00'):
                if awake:
                    self.turn_on("light.entrance_lights",brightness=255,kelvin=2200)
                # elif new == "on" and entity == "binary_sensor.motion_sensor_158d000236a0f3":
                #     self.turn_on("light.entrance_lights",brightness=100,kelvin=2700)
                #     # Entrance lights
                # elif new == "on" and entity == "binary_sensor.motion_sensor_158d000210ca6f":
                #     self.turn_on("light.entrance_lights",brightness=100,kelvin=2700)

        else:
            self.turn_off("light.entrance_lights")
