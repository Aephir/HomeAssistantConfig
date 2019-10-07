import appdaemon.plugins.hass.hassapi as hass

class Alarm(hass.Hass):

    def initialize(self):

        # requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
        # requests.get(self.args.get("autoremote_url", None) + 'get_alarm=:=get')
        self.listen_state(self.test, 'input_boolean.vacation_mode')

    def test(self, entity, attribute, old, new, kwargs):
        requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
        # requests.get('https://autoremotejoaomgcd.appspot.com/sendmessage?key=APA91bHdG9gIIRophSN4rAlk4Y23LJa9o4KH_Q4I44Fzzf3luTHuOITsn0wOwZg3OhfdiPYsjYgWST8ckLapuJPjcHmY4y9G1cHOW96otuGr4M-irV57GXOHP4dC9QVNGcDOckZk2A45&message=get_alarm=:=get')

        #
        # # requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
    #
    # def get_alarm(self, entity, attribute, old, new, kwargs):
    #
    #     self.log('Run hourly test')
    #
    #     requests.get(self.args['autoremote_url'] + 'get_alarm=:=get')
