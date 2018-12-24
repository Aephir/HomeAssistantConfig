# Set status of rooms

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time


class RoomStatus(hass.Hass):

    def initialize(self):

        self.sensors = [
            'binary_sensor.door_window_sensor_158d0002286a78',  # Bathroom window
            'binary_sensor.motion_sensor_158d000210ca6e', # Bathroom motion sensor #1
            'binary_sensor.motion_sensor_158d000236a22f', # Bathroom motion sensor #2
            'sensor.illumination_158d000236a22f', # Bathroom illumination sensor #2
            'sensor.temperature_158d00022c66ff', # Bathroom Xiaomi temperature
            'sensor.humidity_158d00022c66ff', # Bathroom Xiaomi humidity
            'sensor.pressure_158d00022c66ff', # Bathroom Xiaomi pressure
            'sensor.fibaro_system_fgt001_heat_controller_temperature', # Bathroom Fibaro temperature
            'climate.fibaro_system_fgt001_heat_controller_heating', # Bathroom climate
            'light.bathroom' # Bathroom light
            ]

        self.windowSensors = [
            'binary_sensor.door_window_sensor_158d0002286a78'  # Bathroom window
            ]

        self.doorSensors = [
            ''
            ]

        self.motionSensors = [
            'binary_sensor.motion_sensor_158d000210ca6e', # Bathroom motion sensor #1
            'binary_sensor.motion_sensor_158d000236a22f' # Bathroom motion sensor #2
            ]

        self.illuminationSensors = [
            'sensor.illumination_158d000236a22f' # Bathroom illumination sensor #2
            ]

        self.temperatureXiaomi = [
            'sensor.temperature_158d00022c66ff' # Bathroom Xiaomi temperature
            ]

        self.humidityXiaomi = [
            'sensor.humidity_158d00022c66ff' # Bathroom Xiaomi humidity
            ]

        self.pressureXiaomi = [
            'sensor.pressure_158d00022c66ff' # Bathroom Xiaomi pressure
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

        # self.setSensorState(entity = '', attribute = '', old = '', new = '')


        # Makes sure this global variable exists.
        self.anyOpen = None

        # Store time of last opening
        self.lastOpenedTime = ''
        self.lastClosedTime = ''


    def isOpen(self, entity):

        return self.get_state(entity) == "on":


    def setSensorState(self, entity, attribute, old, new, kwargs):

        newStatus = ''
        WindowOpen = self.isOpen('binary_sensor.door_window_sensor_158d0002286a78')
        thermostatStatus = ''
        radiatorTemp = ''
        radiatorOn = ''
        temperature = ''
        humidity = ''
        pressure = ''
        thermostatTemperature = ''

        if entity 'binary_sensor.door_window_sensor_158d0002286a78' and new == "on":
            self.lastOpenedTime = datetime.datetime.now().strftime("%H:%M")
        elif entity 'binary_sensor.door_window_sensor_158d0002286a78' and new == "off":
            self.lastClosedTime = datetime.datetime.now().strftime("%H:%M")

        if self.get_state('binary_sensor.door_window_sensor_158d0002286a78') == 'on':
            newStatus = 'Open'
        else:
            newStatus = 'Closed'

        self.set_state('sensor.bathroom_state', state = newStatus, attributes = {
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
