# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

def toInt(inString):
    try:
        return int(float(inString))
    except ValueError:
        return 0

class PlantProblem(hass.Hass):

    def initialize(self):

        # List of conductivity, moisture, and temperature entity_ids
        self.plant_conductivity_ids = [
            'sensor.plant_sensor_1_conductivity',
            'sensor.plant_sensor_2_conductivity',
            'sensor.plant_sensor_3_conductivity',
            'sensor.plant_sensor_4_conductivity'
            ]

        self.plant_moisture_ids = [
            'sensor.plant_sensor_1_moisture',
            'sensor.plant_sensor_2_moisture',
            'sensor.plant_sensor_3_moisture',
            'sensor.plant_sensor_4_moisture'
            ]

        self.plant_temperature_ids = [
            'sensor.plant_sensor_1_temperature',
            'sensor.plant_sensor_2_temperature',
            'sensor.plant_sensor_3_temperature',
            'sensor.plant_sensor_4_temperature'
            ]

        # list of notify services to use.
        self.device_notify_services = [
            'notify/home_aephir_bot',
            'notify/ios_kristinas_iphone'
            ]

        # Test if any conductivity is an issue
        for entity in self.plant_conductivity_ids:
            self.listen_state(self.conductivity_problem, entity) # conductivity sensors

        # Test if any moisture is an issue
        for entity in self.plant_moisture_ids:
            self.listen_state(self.moisture_problem, entity) # conductivity sensors

        # Test if any temperature is an issue
        for entity in self.plant_temperature_ids:
            self.listen_state(self.temperature_problem, entity) # conductivity sensors

    # Send plant # and type = moisture if any moisture levels are low
    def moisture_problem(self, entity):
        if toInt('sensor.plant_sensor_1_moisture') < self.args["min_moisture_1"]:
            self.messageIs(moisture, one)
        if toInt('sensor.plant_sensor_2_moisture') < self.args["min_moisture_2"]:
            self.messageIs(moisture, two)
        if toInt('sensor.plant_sensor_3_moisture') < self.args["min_moisture_3"]:
            self.messageIs(moisture, three)
        if toInt('sensor.plant_sensor_4_moisture') < self.args["min_moisture_4"]:
            self.messageIs(moisture, four)

    # Send plant # and type = conductivity if any conductivity levels are low
    def conductivity_problem(self, entity):
        if toInt('sensor.plant_sensor_1_conductivity') < self.args["min_conductivity_1"]:
            self.messageIs(conductivity, one)
        if toInt('sensor.plant_sensor_2_conductivity') < self.args["min_conductivity_2"]:
            self.messageIs(conductivity, two)
        if toInt('sensor.plant_sensor_3_conductivity') < self.args["min_conductivity_3"]:
            self.messageIs(conductivity, three)
        if toInt('sensor.plant_sensor_4_conductivity') < self.args["min_conductivity_4"]:
            self.messageIs(conductivity, four)

    # Send plant # and type = temperature if any temperature levels are low
    def temperature_problem(self, entity):
        if toInt('sensor.plant_sensor_1_temperature') < self.args["min_temperature_1"]:
            self.messageIs(temperature, one)
        if toInt('sensor.plant_sensor_2_temperature') < self.args["min_temperature_2"]:
            self.messageIs(temperature, two)
        if toInt('sensor.plant_sensor_3_temperature') < self.args["min_temperature_3"]:
            self.messageIs(temperature, three)
        if toInt('sensor.plant_sensor_4_temperature') < self.args["min_temperature_4"]:
            self.messageIs(temperature, four)

    # Create the message text based on the plant # and the problem.
    def messageIs(self, type, number, **kwargs):
        message_text = ''
        if number == one:
            if type == moisture:
                message_text = 'The ' + self.args["plant_1_name"] + ' plant needs water!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_1_name"] + ' plant needs fertilizer!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_1_name"] + ' plant is cold!'
        elif number == two:
            if type == moisture:
                message_text = 'The ' + self.args["plant_2_name"] + ' needs water!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_2_name"] + ' needs fertilizer!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_2_name"] + ' is cold!'
        elif number == one:
            if type == moisture:
                message_text = 'The ' + self.args["plant_3_name"] + ' plant needs water!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_3_name"] + ' plant needs fertilizer!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_3_name"] + ' plant is cold!'
        elif number == one:
            if type == moisture:
                message_text = 'The ' + self.args["plant_4_name"] + ' plant needs water!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_4_name"] + ' plant needs fertilizer!'
            elif type == conductivity:
                message_text = 'The ' + self.args["plant_4_name"] + ' plant is cold!'
        sendNotification(message_text)

    # Send notification
    def sendNotification(self, message, **kwargs):
        for entity in self.device_notify_services:
            self.call_service(entity, attributes = {"title":"Attention! Your plants are in distress!","message": message})
