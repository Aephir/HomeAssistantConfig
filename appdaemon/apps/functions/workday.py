import appdaemon.plugins.hass.hassapi as hass
import datetime

# Call with:
# workday()

    def workday(self):
        weekday = ''
        vacation = ''
        if datetime.date.weekday(today) < 5:
            weekday = "on"
        else:
            weekday = "off"
        if hass.get_state("input_boolean.vacation_mode") == "on":
            vacation = "on"
        else:
            vacation = "off"
        if weekday == "on" and vacation == "off":
            return True
