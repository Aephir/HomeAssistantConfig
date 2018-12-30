# Generic notifier.
# Use self.set_state("sensor.notify_message", state="blabla") from any other app
# See https://community.home-assistant.io/t/a-notify-function-that-does-more-then-just-1-notify/32483

import appdaemon.plugins.hass.hassapi as hass
import datetime


class Notify(hass.Hass):

    def initialize(self):

        self.motionSensors = self.app_config['global_sensors']['motionSensors']
        self.doorWindowSensors = self.app_config['global_sensors']['doorWindowSensors']

        # self.motionSensors = [
        #     "binary_sensor.motion_sensor_158d00023e3742", # Entrance
        #     "binary_sensor.motion_sensor_158d000200d203", # Basement entrance
        #     "binary_sensor.motion_sensor_158d000236a0f3", # Top floor TV room
        #     "binary_sensor.motion_sensor_158d000236a116", # TV room
        #     "binary_sensor.motion_sensor_158d000200d285", # Conservatory
        #     "binary_sensor.motion_sensor_158d000200e0c5", # Top floor stairway
        #     "binary_sensor.motion_sensor_158d000236a22f", # Bathroom #2
        #     "binary_sensor.motion_sensor_158d000236a0d0", # Upastairs bathroom
        #     "binary_sensor.motion_sensor_158d0001e0a8e1", # Kitchen
        #     "binary_sensor.motion_sensor_158d000210ca6e", # Bathroom #1
        #     "binary_sensor.motion_sensor_158d000210ca6f" # Basemenet stairway
        #     ]

        # self.doorWindowSensors = [
        #     "binary_sensor.door_window_sensor_158d0002286a78", # Bathroom window
        #     "binary_sensor.door_window_sensor_158d000237c924", # Bedroom window
        #     "binary_sensor.door_window_sensor_158d00022b3b66", # Basement door
        #     "binary_sensor.door_window_sensor_158d00022d0917", # Front door
        #     "binary_sensor.door_window_sensor_158d000234dc7b" # Conservatory door
        #     ]

        for entity in self.motionSensors:
            self.listen_state(self.houseEmpty, entity)

        for entity in self.doorWindowSensors:
            self.listen_state(self.houseEmpty, entity)


    def houseEmpty(self, entity, attribute, old, new, kwargs):
        if self.get_state('sensor.home_occupancy') == 'off':
            self.sendNotify(entity, attribute, old, new, kwargs)


    def sendNotify(self, entity, attribute, old, new, kwargs):

        sensor = self.friendly_name(entity)
        message = ''

        self.log('triggered')

        if new == 'on':
            if entity in self.motionSensors:
                message = str(sensor) + ' sensor was triggered at' + str(datetime.datetime.now().strftime("%H:%M"))
                # self.call_service('script.play_dummy_alarm')
            elif entity in self.doorWindowSensors:
                message = str(sensor) + ' was opened at' + str(datetime.datetime.now().strftime("%H:%M"))
                # self.call_service('script.play_dummy_alarm')

        if new == 'off':
            if entity in self.doorWindowSensors:
                message = str(sensor) + ' was closed at' + str(datetime.datetime.now().strftime("%H:%M"))

        self.call_service("notify/home_aephir_bot", message=message)
        self.log('sent')
