# Motion sensors to control the entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

class MotionClass(hass.Hass):

    def initialize(self):
        # Motion sensors.

        self.motion_sensors = [
            "binary_sensor.presence_entrance", # Entrance Motion Sensor
            "binary_sensor.presence_top_floor_stairway", # Top Floor Stairs Motion Sensor
            "binary_sensor.presence_basement_stairway" # Basement Stairway Motion Sensor
            ]

        self.door_sensors = [
            "binary_sensor.openclose_front_door" # Front door
            ]

        self.illumination_sensors = [
            "sensor.lightlevel_entrance" # Entrance Motion Illumination Sensor
            ]

        for entity in self.motion_sensors:
            self.listen_state(self.switch_on, entity, new='on')

        for entity in self.motion_sensors:
            self.listen_state(self.switch_off, entity, new='off')

        for entity in self.door_sensors:
            self.listen_state(self.dooropenclose, entity, new='on')

    # Assess whether we are awake, based on state of entity. Find better proxy eventually.
    def are_we_awake(self, entity):
        if self.get_state(entity) == "on":
            return True

    # Return True/False for whether entity_id has state "on".
    def is_on(self, entity_id):
        return self.get_state(entity_id) == 'on'

    # Returns value of state as integer. Might need to remove the "float" if you get errors.
    def get_integer_state(self, entity_id):
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0


    # If motion on or door open:
    def switch_on(self, entity, attribute, old, new, kwargs):

        workday         = self.get_state('binary_sensor.workday_today')
        workday_tomorrow  = self.get_state('binary_sensor.workday_tomorrow')
        sensor_1_state  = self.get_state("binary_sensor.presence_entrance") # Entrance Motion
        sensor_2_state  = self.get_state("binary_sensor.presence_basement_stairway") # Basement Stairway Motion
        sensor_3_state  = self.get_state("binary_sensor.presence_top_floor_stairway") # Top Floor Stairs Motion Sensor
        sensor_4_state  = self.get_state("binary_sensor.openclose_front_door") # Front door sensor
        awake           = self.are_we_awake("light.living_room_lights")
        party_mode      = self.get_state('input_boolean.party_mode') == 'on'

        if any([sensor_1_state == "on", sensor_2_state == "on", sensor_3_state == "on"]):
            if party_mode:
                self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)
            elif self.now_is_between('07:00:00', '09:00:00'):
                self.turn_on("light.entrance_lights",brightness=100,kelvin=2700)
            elif self.now_is_between('09:00:00', '21:00:00'):
                self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)
            elif self.now_is_between('21:00:00', '23:00:00'):
                if workday_tomorrow:
                    self.turn_on("light.entrance_lights",brightness=75,kelvin=2200)
                else:
                    self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)

            elif self.now_is_between('23:00:00', '07:00:00'):
                if awake:
                    if workday_tomorrow:
                        self.turn_on("light.entrance_lights",brightness=75,kelvin=2200)
                    else:
                        self.turn_on("light.entrance_lights",brightness=255,kelvin=2200)

        elif new == 'on' and entity == 'binary_sensor.openclose_front_door':
            self.turn_on("light.entrance_lights",brightness=255,kelvin=2700)


    # If motion off, and door closed
    def switch_off(self, entity, attribute, old, new, kwargs):

        self.log('test_off')

        sensor_1_state = self.get_state("binary_sensor.presence_entrance") # Entrance Motion
        sensor_2_state = self.get_state("binary_sensor.presence_basement_stairway") # Basement Stairway Motion
        sensor_3_state = self.get_state("binary_sensor.presence_top_floor_stairway") # Top Floor Stairs Motion Sensor
        sensor_4_state = self.get_state("binary_sensor.openclose_front_door") # Front door sensor

        sensor_state    = [sensor_1_state=='off', sensor_2_state=='off', sensor_3_state=='off', sensor_4_state=='off']

        if all(sensor_state):
            self.turn_off("light.entrance_lights")


    # Door open/close
    def dooropenclose(self, entity, attribute, old, new, kwargs):

        sensor_1_state  = self.get_state("binary_sensor.presence_entrance") # Entrance Motion
        sensor_2_state  = self.get_state("binary_sensor.presence_basement_stairway") # Basement Stairway Motion
        sensor_3_state  = self.get_state("binary_sensor.presence_top_floor_stairway") # Top Floor Stairs Motion Sensor
        sensor_4_state  = self.get_state("binary_sensor.openclose_front_door") # Front door sensor

        if new == 'on':
            if self.get_state('light.entrance_lights') == 'off':
                self.switch_on()
        else:
            if all([sensor_1_state=='off', sensor_2_state=='off', sensor_3_state=='off', sensor_4_state=='off']):
                self.switch_off()
