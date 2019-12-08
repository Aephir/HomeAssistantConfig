# Motion sensors to control the entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):
        # Motion sensors.

        self.motionSensors = [
            "binary_sensor.presence_entrance", # Entrance Motion Sensor
            "binary_sensor.presence_top_floor_stairway", # Top Floor Stairs Motion Sensor
            "binary_sensor.presence_basement_stairway" # Basement Stairway Motion Sensor
            ]

        self.doorSensors = [
            "binary_sensor.openclose_front_door" # Front door
            ]

        self.illuminationSensors = [
            "sensor.lightlevel_entrance" # Entrance Motion Illumination Sensor
            ]

        for entity in self.motionSensors:
            self.listen_state(self.switchonoff,entity)

        for entity in self.doorSensors:
            self.listen_state(self.dooropenclose,entity, new='on')

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

        sensor_1_state = self.get_state("binary_sensor.presence_entrance") # Entrance Motion
        sensor_2_state = self.get_state("binary_sensor.presence_basement_stairway") # Basement Stairway Motion
        sensor_3_state = self.get_state("binary_sensor.presence_top_floor_tv_room") # Top Floor Stairs Motion Sensor
        sensor_4_state = self.get_state("binary_sensor.openclose_front_door") # Front door sensor
        awake = self.areWeAwake("light.living_room_lights")
        party_mode      = self.get_state('input_boolean.party_mode') == 'on'

        if sensor_1_state == "on" or sensor_2_state == "on" or sensor_3_state == "on":
            if party_mode:
                self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)
            elif self.now_is_between('07:00:00', '22:00:00'):
                # if self.getIntegerState("sensor.lightlevel_entrance") < 50:
                self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)

            elif self.now_is_between('22:00:00', '07:00:00'):
                if awake:
                    self.turn_on("light.entrance_lights",brightness=255,kelvin=2200)
                # elif new == "on" and entity == "binary_sensor.presence_top_floor_tv_room":
                #     self.turn_on("light.entrance_lights",brightness=100,kelvin=2700)
                #     # Entrance lights
                # elif new == "on" and entity == "binary_sensor.presence_basement_stairway":
                #     self.turn_on("light.entrance_lights",brightness=100,kelvin=2700)

        elif new == 'on' and entity == 'binary_sensor.openclose_front_door':
            self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)

        elif new == 'on' and entity == 'binary_sensor.openclose_front_door':
            pass

        else:
            self.turn_off("light.entrance_lights")

    def dooropenclose(self, entity, attribute, old, new, kwargs):
        if self.get_state('light.entrance_lights') == 'off':
            self.switchonoff()
