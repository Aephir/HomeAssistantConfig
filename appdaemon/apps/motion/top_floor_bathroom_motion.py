# Motion sensors to control the main floor bathroom lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class MotionClass(hass.Hass):

    def initialize(self):
        # Motion detected = lights on; motion stops = lights off.
        self.listen_state(self.switchonoff,"binary_sensor.presence_top_floor_bathroom")
        # Illumination drops while motion sensor is "on" = light on.
        self.listen_state(self.switchonoff,"sensor.lightlevel_top_floor_bathroom")

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

    # If motion sensor_1 detects motion, and turn on light
    # (if day and light levels are low, or turn on dim/red if night and we are not awake).
    def switchonoff(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state("binary_sensor.presence_top_floor_bathroom")
        illumination_1 = self.getIntegerState("sensor.lightlevel_top_floor_bathroom")

        if sensor_1_state == "on":
            if self.now_is_between('07:00:00', '20:30:00'):
                if illumination_1 < 50:
                    self.turn_on("light.top_floor_bathroom",brightness=255,kelvin=2700)

            elif self.now_is_between('20:30:00', '22:00:00'):
                if illumination_1 < 50:
                    self.turn_on("light.top_floor_bathroom",brightness=150,kelvin=2200)

            elif self.now_is_between('22:00:00', '07:00:00'):
                self.turn_on("light.top_floor_bathroom",brightness=25,kelvin=2200)

        else:
            self.turn_off("light.top_floor_bathroom")

# # Get states of motion sensors
# entrance_motion_state = self.get_state("binary_sensor.presence_entrance")
# basement_entrance_motion_state = self.get_state("binary_sensor.presence_basement_entrance")
# basement_stairway_motion_state = self.get_state("binary_sensor.presence_top_floor_tv_room")
# tv_room_motion_state = self.get_state("binary_sensor.presence_tv_room")
# conservatory_motion_state = self.get_state("binary_sensor.presence_conservatory")
# bathroom_1_motion_state = self.get_state("binary_sensor.presence_top_floor_stairway")
# bathroom_2_motion_state = self.get_state("binary_sensor.presence_bathroom_2")
# bathroom_upstairs_motion_state = self.get_state("binary_sensor.presence_top_floor_bathroom")
