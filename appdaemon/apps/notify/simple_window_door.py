import appdaemon.plugins.hass.hassapi as hass


class Notfications(hass.Hass):

    def initialize(self):

        self.window_sensors = {
            'binary_sensor.openclose_bathroom_window': 'bathroom window',
            'binary_sensor.openclose_washing_room_window_1': 'washin room wondow',
            'binary_sensor.openclose_bedroom_window_1': 'bedroom window'

            }

        self.door_sensors = {
            'binary_sensor.openclose_basement_entrance_door': 'basement door',
            'binary_sensor.openclose_front_door': 'fron door',
            'binary_sensor.door_window_sensor_158d000234dc7b': 'conservatory door'
        }

        self.all_sensor =

        self.run_daily(self.notifyEvening, 21:30:00)
        self.run_daily(self.notifyMorning, 21:30:00)

    def notifyEvening(self, entity, attribute, old, new, kwargs):

        list_of_windows, list_of_doors = self.isOpen()
        num_wind = len(list_of_windows)
        num_door = len(list_of_doors)

        message = 'It is now half past nine. The'

        if num_door > 0:
            if num_door > 1:
                for door in range(len(list_of_doors) - 1:):
                    message += ' ' + str(list_of_doors[door]) + (',')
                    if door == len(list_of_doors) - 1:
                        message = message[:-1]
                        message += ' and'
                message += ' are open.'
            else:
                message += ' ' + list_of_doors[0] + ' is open.'
        if num_wind > 0:
            if ' is ' in message:
                message = message[:-8]
            elif ' are ' in message:
                message = message[:-9]
            if num_door > 0:
                message += ' and'

            if num_wind > 1:
                for windows in range(len(list_of_windows) - 1:):
                    message += ' ' + str(list_of_windows[windows])
                    if windows == len(list_of_windows) - 1:
                        message += ' and'
                message += ' are open.'
            elif num_door > 0:
                message += ' are open.'
            else:
                message += ' ' + list_of_doors[0] + ' is open.'

        if num_door + num_wind > 0:
            if self.get_state('device_tracker.meta_walden') == 'home':
                self.call_service('notify/home_aephir_bot', message=message)
            if self.get_state('device_tracker.meta_kristina') == 'home':
            self.call_service("notify/ios_kristinas_iphone", message=message)






    def isOpen(self):

        list_of_windows = []
        list_of_doors = []

        for key in self.window_sensors:
            if self.get_state(key) == 'on':
                list_of_windows += self.window_sensors[key]
        for key in self.door_sensors:
            if self.get_state(key) == 'on':
                list_of_doors += self.door_sensors[key]

        return list_of_windows, list_of_doors
