"""
Warn me if the espresso machine is left "on" for more than 45 minutes.
Notify every 15 minutes.
After 1.5 hours, turn off and notify.
Set times is app config (apps.yaml)
"""

import appdaemon.plugins.hass.hassapi as hass
import datetime

class ApplianceStatus(hass.Hass):


    def initialize(self):
        """
        Initialize the timers and set listen_state.
        """

        self.starttime = datetime.datetime.now()
        self.timer = None
        self.listen_state(self.StartTimer,"switch.switch")


    def StartTimer(self, entity, attribute, old, new, kwargs):
        """
        Cancel timer if entity is turned off.
        Otherwise note the time, and start the loop (SendNotification)
        """

        if new == 'off':
            self.cancel_timer(self.timer) # Cancel for any state change of 'switch.switch'. If I call 'SendNotification' from elsewhere, make this is cancele

        elif new == 'on' and old == 'off':
            if self.timer != None:
                self.cancel_timer(self.timer)
            self.starttime = datetime.datetime.now()
            self.timer = self.run_in(self.SendNotification,self.args["start_after"])
        # else:
        #     self.log("the switch was already on i didnt reset the timer") # For troubleshooting


    def SendNotification(self, kwargs):
        """
        Notify me about leaving the switch on. Repeat every "time_between_notifications" seconds.
        After "end_after" seconds, automatically turn off, and notify me.
        Remember to cancel timer before each recursive callback, as well as after last action ending the loop.
        """

        delta = datetime.datetime.now() - self.starttime
        seconds = int(datetime.timedelta.total_seconds(delta))
        minutes = round(seconds/60)

        # keyboard = [[("Turn Off", "/espresso_off"),
        #              ("I know", "/removekeyboard")]]
        #
        # message = str(self.friendly_name('switch.switch')) + " has been on for " + str(minutes) + " minutes"

        # self.log("Espresso on for " + str(minutes) + " minutes and " + str(seconds) + " seconds.") # for troubleshooting

        if seconds < self.args["end_after"]:

            # self.call_service(self.args['notify'],
            #                     target=self.args["user_id"],
            #                     message=message,
            #                     inline_keyboard=keyboard)

            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes", data={"inline_keyboard":"Turn Off:/espresso_off, I Know:/removekeyboard"})
            # self.call_service('telegram_bot/send_message', message="Espresso machine has been on for " + str(minutes) + " minutes", inline_keyboard = [[("Turn Off","/espresso_off"), ("I Know","/removekeyboard")]])
            self.log("Espresso machine has been on for " + str(minutes) + " minutes")
            # if self.timer != None:
            #     self.cancel_timer(self.timer)
            self.timer = self.run_in(self.SendNotification,self.args["time_between_notifications"])

        else:

            if self.args["switch_off"]:
                self.turn_off(self.args["entity"])
                switchofftext = ", i turned it off."
                self.turn_off('switch.switch')
            else:
                switchofftext = "."
            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes" + switchofftext, data={"inline_keyboard":"Turn back on:/espresso_on, Thanks!:/removekeyboard"})
            # self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes" + switchofftext, inline_keyboard = [[("Turn back on","/espresso_on"), ("OK, thanks!","/removekeyboard")]])
            self.log("Espresso machine has been on for " + str(minutes) + " minutes" + switchoffftext,)
            # if self.timer != None:
            #     self.cancel_timer(self.timer)
