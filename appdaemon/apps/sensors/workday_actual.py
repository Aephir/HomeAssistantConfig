import hassapi as hass

class Sensor(hass.Hass):

    def initialize(self):

        self.run_daily(self.set_workday, "00:00:30")
        self.run_daily(self.set_workday, "19:00:00")
        self.listen_state(self.set_workday, "input_boolean.vacation_mode")


    def set_workday(self, entity, attribute, old, new, kwargs):

        if "binary_sensor.workday_today" == 'on' and "input_boolean.vacation_mode" == 'off':
            workday_today = 'on'
        else:
            workday_today = 'off'

        if "binary_sensor.workday_tomorrow" == 'on' and "input_boolean.vacation_mode" == 'off':
            workday_tomorrow = 'on'
        else:
            workday_tomorrow = 'off'

        # I need a way to set vacation mode for a set period of time that persists between restarts.
        # if self.now_is_between("18:59:00", "19:01:00"):
        #     self.call_service("notify/mobile_app_aephir_s_vog_l29", message="")

        self.set_state("sensor.workday_actual", state = workday_today, attributes = {
            'workday_tomorrow': workday_tomorrow,
            'workday_today': workday_today
                }
            )
