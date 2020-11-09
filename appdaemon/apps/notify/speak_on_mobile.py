import hassapi as hass

class Notify(hass.Hass):

    def initialize(self):

        self.listen_state(self.speak, 'input_boolean.cooking_mode')

        # self.listen_state(self.speak, 'device_tracker.meta_walden', new = 'away')


    def speak(self, entity, attribute, old, new, kwargs):

        # if old == 'home':
        #   title = "you've left the home"

        self.call_service("notify/mobile_app_aephir_s_vog_l29", message='message')
        self.call_service("notify/mobile_app_aephir_s_vog_l29", title='title', message='TTS')



  #
  # - alias: Notify of Motion
  #   trigger:
  #     ...
  #   action:
  #     service: notify.mobile_app_<your_device_id_here>
  #     data:
  #       message: TTS
  #       title: Motion has been detected
