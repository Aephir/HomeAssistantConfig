"""
Notify (actionable) me if the 'entity' is left 'on' for more than 'start_after' seconds.
Notify every 'time_between_notifications' seconds.
After 'end_after' seconds, turn off and notify.
Set variables in app config (apps.yaml)
"""

import appdaemon.plugins.hass.hassapi as hass
import datetime


class NotifyStatus(hass.Hass):

    def initialize(self):
        """
        Initialize the timers and set listen_state.
        """

        self.starttime = datetime.datetime.now()
        self.timer = None
        self.listen_state(self.StartTimer,self.args['entity'])


    def StartTimer(self, entity, attribute, old, new, kwargs):
        """
        Cancel timer if entity is turned 'off'.
        Otherwise note the time, and start the loop (SendNotification)
        """

        if new == 'off':
            self.cancel_timer(self.timer)

        elif new == 'on' and old == 'off':
            if self.timer != None:
                self.cancel_timer(self.timer)
            self.starttime = datetime.datetime.now()
            self.timer = self.run_in(self.SendNotification,self.args['start_after'])


    def SendNotification(self, kwargs):
        """
        Notify me about leaving the 'entity' on. Repeat every 'time_between_notifications' seconds.
        After 'end_after' seconds, if 'switch_off' is True, automatically turn off, and notify me.
        Remember to cancel timer before each recursive callback, as well as after last action ending the loop.
        """

        delta = datetime.datetime.now() - self.starttime
        seconds = int(datetime.timedelta.total_seconds(delta))
        minutes = round(seconds/60)

        keyboard_1 = [[(self.args['button_1'], self.args['command_1']),
                     (self.args['button_3'], self.args['command_3'])],
                    [(self.args['button_2'], self.args['command_2'])]]

        message_1 = str(self.friendly_name(self.args['entity'])) + " has been " + str(self.args["on_open"]) + " for " + str(minutes) + " minutes"

        keyboard_2 = [[(self.args['button_3'], self.args['command_3']),
                     (self.args['button_1'], self.args['command_1'])],
                    [(self.args['button_2'], self.args['command_2'])]]

        notify = self.args['notify']

        if seconds < self.args['end_after']:

            self.call_service(self.args['notify'],
                                title=self.args['title'],
                                target=self.args['user_id'],
                                message=message_1,
                                inline_keyboard=keyboard_1)

            # self.log(self.args['entity'] + " has been on for " + str(minutes) + " minutes") # for troubleshooting
            self.timer = self.run_in(self.SendNotification,self.args['time_between_notifications'])

        else:

            if self.args['switch_off']:
                self.turn_off(self.args['entity'])
                switchofftext = ", i turned it off."
                self.turn_off('switch.switch')

            else:
                switchofftext = "."

            message_2 = str(self.friendly_name(self.args['entity'])) + " has been " + str(self.args["on_open"]) + " for " + str(minutes) + " minutes" + switchofftext

            self.call_service(self.args['notify'],
                                title=self.args['title'],
                                target=self.args['user_id'],
                                message=message_2,
                                inline_keyboard=keyboard_2)

            # self.log(self.args['entity'] + " has been on for " + str(minutes) + " minutes" + switchofftext,) # for troubleshooting
