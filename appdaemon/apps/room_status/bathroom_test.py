# Motion sensors to control the entrance lights.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class RoomStatus(hass.Hass):

    def initialize(self):

        self.sensors = [
            'binary_sensor.openclose_bathroom_window',  # Bathroom window
            'binary_sensor.presence_bathroom', # Bathroom motion sensor #1
            'binary_sensor.presence_bathroom_2', # Bathroom motion sensor #2
            'sensor.lightlevel_bathroom_2', # Bathroom illumination sensor #2
            'sensor.temperature_bathroom', # Bathroom Xiaomi temperature
            'sensor.humidity_bathroom', # Bathroom Xiaomi humidity
            'sensor.pressure_bathroom', # Bathroom Xiaomi pressure
            'sensor.fibaro_system_fgt001_heat_controller_temperature', # Bathroom Fibaro temperature
            'climate.fibaro_system_fgt001_heat_controller_heating', # Bathroom climate
            'light.bathroom' # Bathroom light
            ]

        self.windowSensors = [
            'binary_sensor.openclose_bathroom_window'  # Bathroom window
            ]

        self.doorSensors = [
            ''
            ]

        self.motionSensors = [
            'binary_sensor.presence_bathroom', # Bathroom motion sensor #1
            'binary_sensor.presence_bathroom_2' # Bathroom motion sensor #2
            ]

        self.illuminationSensors = [
            'sensor.lightlevel_bathroom_2' # Bathroom illumination sensor #2
            ]

        self.temperatureXiaomi = [
            'sensor.temperature_bathroom' # Bathroom Xiaomi temperature
            ]

        self.humidityXiaomi = [
            'sensor.humidity_bathroom' # Bathroom Xiaomi humidity
            ]

        self.pressureXiaomi = [
            'sensor.pressure_bathroom' # Bathroom Xiaomi pressure
            ]

        self.temperatureFibaro1 = [
            'sensor.fibaro_system_fgt001_heat_controller_temperature' # Bathroom Fibaro temperature
            ]

        self.temperatureFibaro2 = [
            'sensor.fibaro_system_fgt001_heat_controller_temperature' # Bathroom Fibaro temperature
            ]

        self.climate1 = [
            'climate.fibaro_system_fgt001_heat_controller_heating' # Bathroom climate
            ]

        self.climate1 = [
            '' # Bathroom climate 2
            ]


        for entity in self.sensors:
            self.listen_state(self.setSensorState, entity)


        # Makes sure this global variable exists.
        self.anyOpen = None

        # Store time of last opening
        self.lastOpenedTime = ''
        self.lastClosedTime = ''

        door sensors


    def isOpen(self, entity):

        return self.get_state(entity) == "on":


    def setSensorState(self, entity, attribute, old, new, kwargs):

        newStatus = ''
        WindowOpen = self.isOpen('binary_sensor.openclose_bathroom_window')
        thermostatStatus = ''
        radiatorTemp = ''
        radiatorOn = ''
        temperature = ''
        humidity = ''
        pressure = ''
        thermostatTemperature = ''

        if entity 'binary_sensor.openclose_bathroom_window' and new == "on":
            self.lastOpenedTime = datetime.datetime.now().strftime("%H:%M")
        elif entity 'binary_sensor.openclose_bathroom_window' and new == "off":
            self.lastClosedTime = datetime.datetime.now().strftime("%H:%M")

        if self.get_state('binary_sensor.openclose_bathroom_window') == 'on':
            newStatus = 'Open'
        else:
            newStatus = 'Closed'

        self.set_state('sensor.bathroom', state = newStatus, attributes = {
            'friendly_name': "Bathroom Status",
            'window_open': WindowOpen,
            'thermostat_status': thermostatStatus,
            'radiator_temperature': radiatorTemp,
            'turn_radiator_on_when_window_closes': radiatorOn,
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
            'thermistatTemperature': thermostatTemperature,
            'window_opened_at': self.lastOpenedTime,
            'window_closed_at': self.lastClosedTime
            })
