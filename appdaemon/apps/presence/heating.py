# Heating control

import appdaemon.plugins.hass.hassapi as hass


class HeatingAutomations(hass.Hass):

    def initialize(self):

        self.deviceTrackers = [
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina',
            'input_boolean.guest_mode'
            ]

        self.motionSensors = self.app_config['global_sensors']['motionSensors']

        for entity in self.deviceTrackers:
            self.listen_state(self.heatingLocation, entity)

        for entity in self.motionSensors:
            self.listen_state(self.heatingMotion, entity)



    def heatingLocation(self, entity, attribute, old, new, kwargs):

        coming_home = ''

        if self.workday():
            if old == 'skole' and new == 'away':
                coming_home = True
            else:
                if entity == 'device_tracker.meta_walden':
                    if old == 'work_walden' and new == 'away':
                        coming_home = True
                elif entity == 'device_tracker.meta_kristina':
                    if old == 'work_walden' and new == 'away':
                        coming_home = True

        if coming_home:
            # Heating on.

            # Run in 40 minutes, to see if we arrived home yet.
            self.run_in(self.heatingMotion, 2400)


    def heatingMotion(self, entity, attribute, old, new, kwargs):

        if any(self.motionSensors) == 'on':
            self.heatingOn()

    def areWeHome(self, entity, attribute, old, new, kwargs):
        if any(self.deviceTrackers) == 'home':
            return True

    def heatingOn(self, entity, attribute, old, new, kwargs):

        outdoor_temp = self.get_state('sensor.yr_temperature')
        anything_open = ''
        if any(self.doorWindowSensors) == 'on': # Have this in global functions?
            anything_open = True

        # How to do heating? Control each room individually? Make sure heating is turned off when door/winow is open.

        if self.run_in(self.areWeHome, 2400):
            # Continue heating
            heatingOn
        else:
            # Turn off heating
            heatingOff




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
        else:
            return False
