# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class Test(hass.Hass):


    def initialize(self):
        # Run SendNotification function if switch.switch has been on for 1 hour.
        self.listen_state(self.SendNotification,"input_boolean.vacation_mode", new="on", duration=5) #3600

    # Send a notification to telegram
    def SendNotification(self, entity, attribute, old, new, kwargs):
        # if self.get_state("switch.switch") == "on":
        self.call_service("notify/home_aephir_bot", message="Vacation Mode has been on for 1 hour", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
        self.log("Test Vacation Mode")

#___________________
'''
    def initialize(self):

        # List of entity_ids
        self.test_ids = [
            'input_boolean.vacation_mode'
            ]

        # list of notify services to use.
        self.device_notify_services = [
            'notify/home_aephir_bot'
            ]

        # Get state change
        for entity in self.test_ids:
            self.listen_state(self.sendNotification, entity)

    # Send notification
    def sendNotification(self, entity, attribute, old, new, test, **kwargs):
        for entity in self.device_notify_services:
            self.call_service(entity, message="Switched on Vacation Mode", data={"inline_keyboard":"Turn off guest mode:/guest_mode_off, No action:/removekeyboard"})
'''

    # # Send plant # and type = moisture if any moisture levels are low
    # def moisture_problem(self, entity):
    #     if toInt('sensor.plant_sensor_1_moisture') < self.args["min_moisture_1"]:
    #         self.messageIs(moisture, one)
    #     if toInt('sensor.plant_sensor_2_moisture') < self.args["min_moisture_2"]:
    #         self.messageIs(moisture, two)
    #     if toInt('sensor.plant_sensor_3_moisture') < self.args["min_moisture_3"]:
    #         self.messageIs(moisture, three)
    #     if toInt('sensor.plant_sensor_4_moisture') < self.args["min_moisture_4"]:
    #         self.messageIs(moisture, four)
    #
    # # Send plant # and type = conductivity if any conductivity levels are low
    # def conductivity_problem(self, entity):
    #     if toInt('sensor.plant_sensor_1_conductivity') < self.args["min_conductivity_1"]:
    #         self.messageIs(conductivity, one)
    #     if toInt('sensor.plant_sensor_2_conductivity') < self.args["min_conductivity_2"]:
    #         self.messageIs(conductivity, two)
    #     if toInt('sensor.plant_sensor_3_conductivity') < self.args["min_conductivity_3"]:
    #         self.messageIs(conductivity, three)
    #     if toInt('sensor.plant_sensor_4_conductivity') < self.args["min_conductivity_4"]:
    #         self.messageIs(conductivity, four)
    #
    # # Send plant # and type = temperature if any temperature levels are low
    # def temperature_problem(self, entity):
    #     if toInt('sensor.plant_sensor_1_temperature') < self.args["min_temperature_1"]:
    #         self.messageIs(temperature, one)
    #     if toInt('sensor.plant_sensor_2_temperature') < self.args["min_temperature_2"]:
    #         self.messageIs(temperature, two)
    #     if toInt('sensor.plant_sensor_3_temperature') < self.args["min_temperature_3"]:
    #         self.messageIs(temperature, three)
    #     if toInt('sensor.plant_sensor_4_temperature') < self.args["min_temperature_4"]:
    #         self.messageIs(temperature, four)

# import appdaemon.plugins.hass.hassapi as hass
# import time
#
#
# class EspressoStatus(hass.Hass):
#
#     def initialize(self):
#         # Run SendNotification function if switch.switch has been on for 1 hour.
#         self.listen_state(self.SendNotification,"switch.switch", new="on") #3600
#
#
#     # Send a notification to telegram
#     def SendNotification(self, entity, attribute, old, new, kwargs):
#         time.sleep(3600)
#         if self.get_state("switch.switch") == "on":
#             self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1 hour", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
#             self.log("Espresso machine has been on for 1 hour")
#             time.sleep(30)
#             if self.get_state("switch.switch") == "on":
#                 time.sleep(1800)
#                 if self.get_state("switch.switch") == "on":
#                     self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1.5 hours", data={"inline_keyboard":"Turn off:/espresso_off, No action:/removekeyboard"})
#                     self.log("Espresso machine has been on for 1.5 hours")
#                     time.sleep(30)
#                     if self.get_state("switch.switch") == "on":
#                         time.sleep(1800)
#                         if self.get_state("switch.switch") == "on":
#                             self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for 1 hour", data={"inline_keyboard":"Turn back on:/espresso_on, No action:/removekeyboard"})
#                             self.log("Espresso machine has been on for 2 hours")
