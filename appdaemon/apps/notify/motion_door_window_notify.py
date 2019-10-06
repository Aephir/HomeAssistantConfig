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
        #     "binary_sensor.presence_entrance", # Entrance
        #     "binary_sensor.presence_basement_entrance", # Basement entrance
        #     "binary_sensor.presence_top_floor_tv_room", # Top floor TV room
        #     "binary_sensor.presence_tv_room", # TV room
        #     "binary_sensor.presence_conservatory", # Conservatory
        #     "binary_sensor.presence_top_floor_stairway", # Top floor stairway
        #     "binary_sensor.presence_bathroom_2", # Bathroom #2
        #     "binary_sensor.presence_top_floor_bathroom", # Upastairs bathroom
        #     "binary_sensor.presence_kitchen", # Kitchen
        #     "binary_sensor.presence_bathroom", # Bathroom #1
        #     "binary_sensor.presence_basement_stairway" # Basemenet stairway
        #     ]

        # self.doorWindowSensors = [
        #     "binary_sensor.openclose_bathroom_window", # Bathroom window
        #     "binary_sensor.openclose_bedroom_window_1", # Bedroom window
        #     "binary_sensor.openclose_basement_entrance_door", # Basement door
        #     "binary_sensor.openclose_front_door", # Front door
        #     "binary_sensor.door_window_sensor_158d000234dc7b" # Conservatory door
        #     ]

        for entity in self.motionSensors:
            self.listen_state(self.houseEmpty, entity)

        for entity in self.doorWindowSensors:
            self.listen_state(self.houseEmpty, entity)


    def houseEmpty(self, entity, attribute, old, new, kwargs):
        if self.get_state('sensor.home_occupancy') == 'on':
            self.sendNotify(entity, attribute, old, new, kwargs)


    def sendNotify(self, entity, attribute, old, new, kwargs):

        # sensor = self.friendly_name(entity)
        # message = ''

        # keyboard = [[(self.args["button_1"], self.args["command_1"]),
        #              (self.args["button_3"], self.args["command_3"])],
        #             [(self.args["button_2"], self.args["command_2"])]]


        self.log('triggered')

        if new == 'on':
            if entity in self.motionSensors:
                message = str(self.friendly_name(entity)) + ' was triggered at' + str(datetime.datetime.now().strftime("%H:%M"))
                # message = str(sensor) + ' sensor was triggered at' + str(datetime.datetime.now().strftime("%H:%M"))
                # self.call_service('script.play_dummy_alarm')
            elif entity in self.doorWindowSensors:
                message = str(self.friendly_name(entity)) + ' was opened at' + str(datetime.datetime.now().strftime("%H:%M"))
                # message = str(sensor) + ' was opened at' + str(datetime.datetime.now().strftime("%H:%M"))
                # self.call_service('script.play_dummy_alarm')

        if new == 'off':
            if entity in self.doorWindowSensors:
                message = str(self.friendly_name(entity)) + ' was closed at' + str(datetime.datetime.now().strftime("%H:%M"))
                # message = str(sensor) + ' was closed at' + str(datetime.datetime.now().strftime("%H:%M"))

        self.call_service(self.args['notify'],
                            title=self.args["title"],
                            target=self.args["user_id"],
                            message=message
                            # inline_keyboard=keyboard_1)
        # self.call_service(self.args['notify_who'], message=message)
        # self.log('sent')
