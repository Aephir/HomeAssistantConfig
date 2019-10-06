# import appdaemon.plugins.hass.hassapi as hass
# import datetime
#
# # Call with:
# # workday()
#
# class Workday(hass.Hass):

def workday():

    normal_workday = self.get_state("binary_sensor.workday") == "on"
    vacation = self.get_state("input_boolean.vacation_mode") == "on"

    if normal_workday and not vacation:
        return True
