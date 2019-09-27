# Hue tap button

import appdaemon.plugins.hass.hassapi as hass
import datetime

class Remote(hass.Hass):


    def initialize(self):
        # Detect click. It detects sequential clicks of same button! (Why/how?)

        self.sensors = [
            'binary_sensor.door_window_sensor_158d00022d0917', # Front door
            'binary_sensor.door_window_sensor_158d00022b3b66'] # Basement door

        self.listen_state(self.button_click,self.args["entityID"])
        # self.listen_state(self.girls_night,self.args["entityID"])

    #
    # def girls_night(self, entity, attribute, old, new, kwargs):
    #
    #     top_floor_lights = [
    #         'light.top_floor_hallway',
    #         'light.top_floor_tv_area'
    #         ]
    #
    #     for light in top_floor_lights:
    #         self.toggle(light)


    def whatsUp(self, entity, attribute, old, new, kwargs):

        weekday = date.today().weekday() < 5
        workday = weekday and self.get_state('input_boolean.vacation_mode') == 'off'

        if workday:
            if self.now_is_between("06:00:00", "10:00:00"):
                morning = True
            else:
                morning = False
        else:
            if self.now_is_between("06:00:00", "11:00:00"):
                morning = True
            else:
                morning = False

        if workday:
            if self.now_is_between("18:00:00", "01:00:00"):
                evening = True
            else:
                evening = False
        else:
            if self.now_is_between("18:00:00", "05:00:00"):
                evening = True
            else:
                evening = False

        if entity in self.sensors and morning:
            self.leaving()
        elif entity == self.args["entityID"] and evening:
            self.goingToBed()
        elif entity == self.args["entityID"] and morning:
            self.morningRoutine()



    def leaving(self, entity, attribute, old, new, kwargs):

        windows_open = self.get_state('sensor.windows_and_doors', attribute = 'number_of_windows')
        doors_open = self.get_state('sensor.windows_and_doors', attribute = 'number_of_doors')

        if windows_open > 0 or doors_open > 0:
            any_open = True

        if any_open:
            self.notifyForgotten()


    def button_click(self, entity, attribute, old, new, kwargs):
        if self.now_is_between("06:00:00", "18:00:00"):
            self.turn_on(self.args["entityID1"])
        else:
            self.turn_off(self.args["entityID2"])
            self.turn_off("media_player.ue46es8005")


    def goodNightRoutine(self):

        now     = datetime.datetime.now()
        if datetime.date.today().weekday() < 5:
            weekday = True
        else:
            weekday = False


    def notifyForgotten(self):

        list_of_open = self.get_state('sensor.windows_and_doors', attributes='list_of_open')

        if len(self.get_state('sensor.windows_and_doors', attributes='list_of_open')) > 1:
            self.call_service("notify/home_aephir_bot", message="You have left the following doors and/or windows open")
        elif len(self.get_state('sensor.windows_and_doors', attributes='list_of_open')) == 1:
            open = str(self.get_state('sensor.windows_and_doors', attributes='list_of_open'))
            self.call_service("notify/home_aephir_bot", message="You have left the " + open + " open")
