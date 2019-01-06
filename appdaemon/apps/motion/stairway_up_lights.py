"""
Motion sensors to control the stairway lights going up.
"""

import appdaemon.plugins.hass.hassapi as hass

class MotionClass(hass.Hass):

    def initialize(self):
        # Motion sensors.

        self.motion_sensors = [
            "binary_sensor.motion_sensor_158d00023e3742", # Entrance Motion Sensor
            "binary_sensor.motion_sensor_158d000200e0c5" # Top Floor Stairs Motion Sensor
            ]

        self.illumination_sensors = [
            "sensor.illumination_158d000200e0c5" # Top Floor Stairs Motion Illumination Sensor
            ]

        for entity in self.motion_sensors:
            self.listen_state(self.motionTrigger,entity)

        for entity in self.illumination_sensors:
            self.listen_state(self.motionTrigger,entity)


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
        sensor_2_state = self.get_state("binary_sensor.motion_sensor_158d000200e0c5") # Top Floor Stairs Motion Sensor

        awake = self.areWeAwake("light.living_room_lights")

        if entity == "binary_sensor.motion_sensor_158d00023e3742" and new == 'on':
            if sensor_1_state == 'off':
                if self.now_is_between('07:00:00', '22:00:00'):
                    self.turn_on("light.stairway_up",brightness=255,kelvin=2700)
                elif self.now_is_between('22:00:00', '07:00:00'):
                    if awake:
                        self.turn_on("light.stairway_up",brightness=255,kelvin=2700)
                    else:
                        self.turn_on("light.stairway",brightness=10,kelvin=2200)

        elif entity == "binary_sensor.motion_sensor_158d000200e0c5" and new == 'on':
            if sensor_1_state == 'off':
                if self.now_is_between('07:00:00', '22:00:00'):
                    if self.getIntegerState("sensor.illumination_158d000200e0c5") < 50:
                        self.turn_on("light.stairway_up",brightness=255,kelvin=2700)

                elif self.now_is_between('22:00:00', '07:00:00'):
                    if awake:
                        self.turn_on("light.stairway_up",brightness=255,kelvin=2700)
                    else:
                        self.turn_on("light.stairway",brightness=50,kelvin=2200)

        elif sensor_1_state == 'on' and sensor_2_state == 'on': # in the off chance that one motion sensor triggers, and the next is turned on before the check is performed.
            self.turn_on("light.stairway_up",brightness=255,kelvin=2700)

        elif sensor_1_state == 'off' and sensor_2_state == 'off':
            self.turn_off("light.stairway_up")
