import appdaemon.plugins.hass.hassapi as hass
import datetime

class OccupancyAutomations(hass.Hass):

    def initialize(self):

        self.door_sensors = [
            'binary_sensor.door_window_sensor_158d00022b3b66', # Basement door
            'binary_sensor.door_window_sensor_158d00022d0917', # Front door
            'binary_sensor.door_window_sensor_158d000234dc7b'
            ]

        for i in self.door_sensors:
            self.listen_state(self.notifyForgotten, i, new='on')


    def notifyForgotten(self, entity, attribute, old, new, kwargs):

        number_open_doors   = str(self.get_state('sensor.windows_and_doors', attribute='number_of_doors'))
        number_open_windows = str(self.get_state('sensor.windows_and_doors', attribute='number_of_windows'))
        list_open           = self.get_state('sensor.windows_and_doors', attribute='list_of_open')
        message             = ''
        convert             = {'binary_sensor.door_window_sensor_158d00022d0917':'Front door',
                               'binary_sensor.door_window_sensor_158d00022b3b66':'Basement door'}

        # self.log('This was a triumph')
        # self.log(number_open_doors)
        # self.log(number_open_windows)
        # self.log(list_open)

        if len(list_open) > 1:
            if datetime.date.today().weekday() < 5:
                if self.now_is_between("05:30:00", "09:00:00"):
                    if new == 'on':
                        window  = ''
                        door    = ''
                        message = 'Doors/windows are open. If you\'re leaving, please close the'

                        for i in range(len(list_open)):
                            if i != convert[entity]:
                                message += ' ' + list_open[i] + ','
                            # message_2 = message.replace(convert[entity], '')
                        message2 = message[:-1]

                        if self.get_state(self.args['tracker_1']) == 'home':
                            self.call_service(self.args['notify_1'], message=message3)
                        if self.get_state(self.args['tracker_2']) == 'home':
                            self.call_service(self.args['notify_2'], message=message3)

            # else:
