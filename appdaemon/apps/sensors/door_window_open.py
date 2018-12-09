# Create sensors

import appdaemon.plugins.hass.hassapi as hass


class Sensor(hass.Hass):

    def initialize(self):

        self.doorList = [
            'binary_sensor.door_window_sensor_158d00022b3b66', # Basement door
            'binary_sensor.door_window_sensor_158d00022d0917', # Front door
            'binary_sensor.door_window_sensor_158d000234dc7b'  # Conservatory door
            ]

        self.shedDoor = [
            'binary_sensor.neo_coolcam_doorwindow_detector_sensor'
            ]

        self.windowList = [
            'binary_sensor.door_window_sensor_158d000237c924', # Bedroom window
            'binary_sensor.door_window_sensor_158d0002286a78'  # Bathroom window
            ]

        self.friendlyName = {
            'binary_sensor.door_window_sensor_158d00022b3b66': 'Basement door',
            'binary_sensor.door_window_sensor_158d00022d0917': 'Front door',
            'binary_sensor.door_window_sensor_158d000234dc7b': 'Conservatory door',
            'binary_sensor.neo_coolcam_doorwindow_detector_sensor': 'Shed door',
            'binary_sensor.door_window_sensor_158d000237c924': 'Bedroom window',
            'binary_sensor.door_window_sensor_158d0002286a78': 'Bathroom window'
            }

        self.anyOpen = None

        for entity in self.windowList:
            self.listen_state(self.setSensorState, entity)

        for entity in self.doorList:
            self.listen_state(self.setSensorState, entity)


    def isOpen(self, entity, attribute, old, new, kwargs):

        self.anyOpen = []

        for entity in self.doorList:
            if self.get_state(entity) == "on":
                self.anyOpen.append(self.friendlyName[entity])

        for entity in self.windowList:
            if self.get_state(entity) == "on":
                self.anyOpen.append(self.friendlyName[entity])

        return self.anyOpen


    def setSensorState(self, entity, attribute, old, new, kwargs):

        sensorName = ''
        newStatus = ''
        numberOfDoors = 0
        numberOfWindows = 0
        shedDoor = ''
        newStatus = ''
        isOpen = self.isOpen(entity, attribute, old, new, kwargs)

        for entity in self.doorList:
            if self.get_state(entity) == "on":
                numberOfDoors += 1

        for entity in self.windowList:
            if self.get_state(entity) == "on":
                numberOfWindows += 1

        if self.get_state(self.shedDoor[0]) == "on":
            shedDoor = 'Open'
        elif self.get_state(self.shedDoor[0]) == "off":
            shedDoor = 'Closed'
        else:
            shedDoor = "Unknown"

        if numberOfDoors > 0 or numberOfWindows > 0:
            newStatus = 'Open'
        else:
            newStatus = 'Closed'

        self.set_state('sensor.windows_and_doors', state = newStatus, attributes = {
            'friendly_name': "Open doors and windows",
            'number_of_doors': numberOfDoors,
            'number_of_windows': numberOfWindows,
            'shed_door': shedDoor,
            'list_of_open': self.anyOpen
            })
