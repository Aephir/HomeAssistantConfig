import hassapi as hass

class ApplianceStatus(hass.Hass):

    def initialize(self):

        sensors =   [
                    'binary_sensor.washer_error_state',
                    'binary_sensor.washer_wash_completed'
                    # 'sensor.washer'
                    ]

        for sensor in sensors:
            self.listen_state(self.notify_finished_wash, sensor) # , attribute='all'

    def notify_finished_wash(self, entity, attribute, old, new, kwargs):

        message = ''

        if entity == 'binary_sensor.washer_wash_completed' and new == 'on':
            message = 'Vaskemaskinen er færdig.'
        elif entity == 'binary_sensor.washer_error_state' and new == 'on':
            message = 'Vaskemaskinen melder fejl!'

        if message != '':
            self.call_service('notify/home_aephir_bot', message=message)
            self.call_service("notify/ios_kristinas_iphone", message=message)
