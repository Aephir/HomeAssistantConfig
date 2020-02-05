# Motion sensors to control the entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):

        self.motionSensors = [
            "binary_sensor.presence_top_floor_stairway" # Top floor stairway
            ]

        for entity in self.motionSensors:
            self.listen_state(self.switchOnOff,entity)

        self.timer = None

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
    def switchOnOff(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state("binary_sensor.presence_top_floor_stairway") # Top Floor Stairs Motion
        sensor_2_state = self.get_state("binary_sensor.presence_basement_stairway") # Basement Stairway Motion
        sensor_3_state = self.get_state("binary_sensor.presence_entrance") # Entrance Motion
        sensor_4_state = self.get_state("binary_sensor.presence_top_floor_tv_room") # Top Floor TV Room Motion
        awake = self.areWeAwake("light.living_room._lights")
        party_mode = self.get_state('input_boolean.party_mode') == 'on'

        if party_mode:
            self.turn_on("light.stairway_up",brightness=255,kelvin=2700)

        elif sensor_1_state == "on":
            if self.now_is_between('07:00:00', '22:00:00'):
                self.turn_on("light.stairway_up",brightness=255,kelvin=2700)
            elif self.now_is_between('22:00:00', '07:00:00'):
                if sensor_4_state == "on": # Meaning someone likel came from TV area, and are going down.
                    self.turn_on("light.stairway_up",brightness=100,kelvin=2700)
                elif awake:
                    self.turn_on("light.stairway_up",brightness=255,kelvin=2700)
                else:
                    self.turn_on("light.stairway_up",brightness=25,kelvin=2700)
            # self.cancel_timer(self.timer)
            # self.timer = self.run_in(self.lightOff, 300)
        elif sensor_1_state == "off" and sensor_2_state == "off" and sensor_3_state == "off" and sensor_4_state == "off":
            self.turn_off("light.stairway_up")
            self.turn_off("light.stairway_down")
            self.turn_off("light.top_floor_hallway")
            self.turn_off("light.top_floor_tv_area")
        elif sensor_1_state == "off" and sensor_2_state == "off" and sensor_3_state == "off":
            self.turn_off("light.stairway_up")
            self.turn_off("light.stairway")
            self.turn_off("light.top_floor_hallway")
        elif sensor_1_state == "off" and sensor_3_state == "off":
            self.turn_off("light.stairway_up")

    def lightOff(self, entity, attribute, old, new, kwargs):
        self.turn_off("light.top_floor_hallway")
