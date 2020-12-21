"""
Xiaomi Single button #1
"""

import appdaemon.plugins.hass.hassapi as hass

class Remote(hass.Hass):

    def initialize(self):

        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])
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


    def button_click(self, event_name, data, kwargs):
        """
        data['event'] is in the format 'X00Y', where:

            1000    = Button down
            1002    = Button up
            1001    = Button hold
            1003    = Button hold up
        """

        workday             = self.get_state('sensor.workday_actual') == 'on'
        workday_tomorrow    = self.get_state('sensor.workday_actual', attribute='workday_tomorrow') == 'on'
        open                = self.get_state('sensor.windows_and_doors') == 'Open'
        if open:
            list_of_open    = self.get_state('sensor.windows_and_doors', attribute='list_of_open')
        walden_home         = self.get_state('device_tracker.meta_walden') == 'home'
        kristina_home       = self.get_state('device_tracker.meta_kristina') == 'home'

        # if self.now_is_between("20:30:00", "00:00:00") and
        #     self.get_state('binary_sensor.workday_tomorrow') == 'on' and
        #     self.get_state('input_boolean.vacation_mode') == 'off' or
        #     self.now_is_between("00:00:00", "05:00:00") and
        #     self.get_state('binary_sensor.workday_today') == 'on' and
        #     self.get_state('input_boolean.vacation_mode') == 'off':
        #     work = True
        # else:
        #     work = False

        if data['id'] == self.args['id']: # Single button
            if data['event'] == 1002: # Button 1 up
                if self.now_is_between("06:00:00", "14:00:00"):
                    self.turn_on(self.args["coffee"])

                elif self.now_is_between("18:00:00", "20:00:00"):
                    for i in self.args['adult_media']:
                        self.turn_off(i)
                    if open:
                        if walden_home:
                            self.notify('notify/mobile_app_aephir_s_vog_l29', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                        elif kristina_home:
                            self.notify('notify/mobile_app_kristina_iphone11', message='Remember, the following windows and doors are open: ' + str(list_of_open))

                elif self.now_is_between("20:00:00", "21:00:00"):
                    for i in self.args['adult_media']:
                        self.turn_off(i)
                    if open:
                        if walden_home:
                            self.notify('notify/mobile_app_aephir_s_vog_l29', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                        elif kristina_home:
                            self.notify('notify/mobile_app_kristina_iphone11', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                    if  workday_tomorrow:
                        for i in self.args['kid_media']:
                            self.turn_off(i)
                        for i in self.args['naia_media']:
                            self.turn_off(i)

                elif self.now_is_between("21:00:00", "22:00:00"):
                    for i in self.args['adult_media']:
                        self.turn_off(i)
                    if open:
                        if walden_home:
                            self.notify('notify/mobile_app_aephir_s_vog_l29', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                        elif kristina_home:
                            self.notify('notify/mobile_app_kristina_iphone11', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                    if  workday_tomorrow:
                        for i in self.args['kid_media']:
                            self.turn_off(i)
                        for i in self.args['naia_media']:
                            self.turn_off(i)

                elif self.now_is_between("22:00:00", "05:45:00"):
                    for i in self.args['adult_media']:
                        self.turn_off(i)
                    self.notify('notify/mobile_app_aephir_s_vog_l29', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                    if open:
                        if walden_home:
                            self.notify('notify/mobile_app_aephir_s_vog_l29', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                        elif kristina_home:
                            self.notify('notify/mobile_app_kristina_iphone11', message='Remember, the following windows and doors are open: ' + str(list_of_open))
                    if  workday_tomorrow:
                        for i in self.args['kid_media']:
                            self.turn_off(i)
                        for i in self.args['naia_media']:
                            self.turn_off(i)
                        for i in self.args['emilie_media']:
                            self.turn_off(i)

            # elif data['event'] == 1003:
            #     Something
