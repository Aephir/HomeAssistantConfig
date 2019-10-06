"""
Check whether it is a workday when we have to get up
regardless of whether it is before or after midnight.
"""
import appdaemon.plugins.hass.hassapi as hass

class Global(hass.Hass):

    def test_function(self):

        return 'I can call the function from Global Functions!'


    def workday_when_waking(self):
        """
        Returns True if there is work in the morning, False if not.
        """
        return self.now_is_between("12:00:00", "00:00:00") and
            self.get_state('binary_sensor.workday_tomorrow') == 'on' and
            self.get_state('input_boolean.vacation_mode') == 'off' or
            self.now_is_between("00:00:00", "08:00:00") and
            self.get_state('binary_sensor.workday_today') == 'on' and
            self.get_state('input_boolean.vacation_mode') == 'off'


    def get_integer_state(entity_id):
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0
