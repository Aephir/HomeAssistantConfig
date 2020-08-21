import hassapi as hass

class ApplianceStatus(hass.Hass):

    def initialize(self):

        self.timer = None
        self.message = ''

        sensors =   [
                    'binary_sensor.refrigerator_door_open',
                    'sensor.refrigerator'
                    ]

        for sensor in sensors:
            self.listen_state(self.fridge_status, sensor)

    def fridge_status(self, entity, attribute, old, new, kwargs):

        if entity == 'sensor.refrigerator' and new == 'off':
            self.message = 'Kølseskabet er slukket!'
            self.notify()
        elif entity == 'binary_sensor.refrigerator_door_open':
            self.message = 'Kølseskabets dør har været åben i 90 sekunder!'
            self.timer = self.run_in(self.notify, 90)

    def notify(self):

        self.cancel_timer(self.timer)
        self.call_service('notify/home_aephir_bot', message=self.message)
        self.call_service("notify/ios_kristinas_iphone", message=self.message)
