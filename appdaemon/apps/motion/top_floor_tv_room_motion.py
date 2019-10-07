# Motion sensors to control the entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):

        self.motionSensors = [
            "binary_sensor.presence_top_floor_stairway", # Top floor stairway
            "binary_sensor.presence_top_floor_tv_room"  # Top floor tv room
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

        if new == "on" and entity == "binary_sensor.presence_top_floor_tv_room": # If top floor TV room motion is triggered
            if sensor_1_state == "on": # When top floor stairway is also on (meaning someone likel came up the stairs)
                if self.now_is_between('07:00:00', '20:00:00'):
                    self.turn_on("light.top_floor_tv_area",brightness=255,kelvin=2700)
                    self.turn_on("light.top_floor_hallway",brightness=255,kelvin=2700)
                    # self.cancel_timer(self.timer)
                    # self.timer = self.run_in(self.lightOff, 1800)
                elif self.now_is_between('20:00:00', '21:30:00'):
                    self.turn_on("light.top_floor_tv_area",brightness=100,kelvin=2700)
                    self.turn_on("light.top_floor_hallway",brightness=100,kelvin=2700)
                elif self.now_is_between('21:30:00', '07:00:00'):
                    self.turn_on("light.top_floor_tv_area",brightness=10,kelvin=2700)
                    self.turn_on("light.top_floor_hallway",brightness=100,kelvin=2700)
            else:
                if self.now_is_between('07:00:00', '20:00:00'):
                    self.turn_on("light.top_floor_tv_area",brightness=255,kelvin=2700)
                    self.turn_on("light.top_floor_hallway",brightness=255,kelvin=2700)
                    # self.cancel_timer(self.timer)
                    # self.timer = self.run_in(self.lightOff, 1800)
                elif self.now_is_between('20:00:00', '21:30:00'):
                    self.turn_on("light.top_floor_tv_area",brightness=100,kelvin=2700)
                    self.turn_on("light.top_floor_hallway",brightness=100,kelvin=2700)
                elif self.now_is_between('21:30:00', '07:00:00'):
                    self.turn_on("light.top_floor_tv_area",brightness=10,kelvin=2700)

        elif new == "off":
            if sensor_1_state == "off" and sensor_4_state == "off":
                self.turn_off("light.top_floor_tv_area")
                self.turn_off("light.top_floor_hallway")
            elif sensor_1_state == "off":
                self.turn_off("light.top_floor_hallway")
            elif sensor_4_state == "off":
                self.turn_off("light.top_floor_tv_area")



    #             self.cancel_timer(self.timer)
    #             self.timer = self.run_in(self.lightOff, 300)
    #         elif sensor_1_state == "off" and sensor_3_state == "off":
    #             self.turn_off("light.stairway_up")
    #
    # def lightOff(self, entity, attribute, old, new, kwargs):
    #     self.turn_off("light.top_floor_hallway")
