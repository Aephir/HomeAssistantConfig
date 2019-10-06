# Set status of rooms

import appdaemon.plugins.hass.hassapi as hass
import datetime

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

        # self.climate2 = [
        #     '' # Bathroom climate 2
        #     ]


        for entity in self.sensors:
            self.listen_state(self.setSensorState, entity)

        # Makes sure this global variable exists.
        self.anyOpen = None

        # Store time of last opening
        self.lastOpenedTime = ''
        self.lastClosedTime = ''


    def isOpen(self, entity):

        return self.get_state(entity) == "on"


    def setSensorState(self, entity, attribute, old, new, kwargs):

        newStatus = ''
        WindowOpen = self.isOpen('binary_sensor.openclose_bathroom_window')
        thermostatStatus = self.get_state('climate.fibaro_system_fgt001_heat_controller_heating')
        radiatorTemp = self.get_state('climate.fibaro_system_fgt001_heat_controller_heating.temperature')
        radiatorState = ''
        temperature = self.get_state('sensor.temperature_bathroom')
        humidity = self.get_state('sensor.humidity_bathroom')
        pressure = self.get_state('sensor.pressure_bathroom')
        thermostatTemperature = self.get_state('sensor.fibaro_system_fgt001_heat_controller_temperature')

        if entity == 'binary_sensor.openclose_bathroom_window' and new == 'on' and old == 'off':
            self.lastOpenedTime = datetime.datetime.now().strftime("%H:%M")
            radiatorState = self.get_state('climate.fibaro_system_fgt001_heat_controller_heating')
        elif entity == 'binary_sensor.openclose_bathroom_window' and new == 'off' and old == 'on':
            self.lastClosedTime = datetime.datetime.now().strftime("%H:%M")

        if self.get_state('binary_sensor.openclose_bathroom_window') == 'on':
            newStatus = 'Open'
        else:
            newStatus = 'Closed'

        self.set_state('sensor.bathroom_state', state = newStatus, attributes = {
            'friendly_name': "Bathroom Status",
            'window_open': WindowOpen,
            'thermostat_status': thermostatStatus,
            'radiator_temperature': radiatorTemp,
            'radiator_state_when_window_closes': radiatorState,
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
            'thermostat_temperature': thermostatTemperature,
            'window_opened_at': self.lastOpenedTime,
            'window_closed_at': self.lastClosedTime
            })
