import appdaemon.plugins.hass.hassapi as hass

class TelegramBotEventListener(hass.Hass):
    """
    Event listener for Telegram callbacks.
    """

    def initialize(self):
        """
        Listen to Telegram events of interest.
        """
        # self.listen_event(self.receive_telegram_command, 'telegram_command')
        self.listen_event(self.receive_telegram_callback, 'telegram_callback')


    def receive_telegram_callback(self, event_id, payload_event, *args):
        """
        Match telegram commands with actions.
        """
        self.log(payload_event)
        if payload_event['data'] == '/espresso_on':
            self.turn_on('switch.switch')
        if payload_event['data'] == '/espresso_off':
            self.turn_off('switch.switch')
        if payload_event['data'] == '/fountain_on':
            self.turn_on('switch.fountain')
        if payload_event['data'] == '/fountain_off':
            self.turn_off('switch.fountain')
        if payload_event['data'] == '/lights_off':
            self.turn_on('script.scene_all_lights_off')
        if payload_event['data'] == '/all_off':
            self.turn_on('script.everyone_left_turn_off_everything')
        if payload_event['data'] == '/set_alarm_away':
            self.turn_on('script.alarm_armed_away')
        if payload_event['data'] == '/set_alarm_all_off':
            self.turn_on('script.alarm_armed_away')
            self.turn_on('script.everyone_left_turn_off_everything')
        if payload_event['data'] == '/guest_mode_off':
            self.turn_off('input_boolean.guest_mode')

    def removeKeyboard(self, event_id, payload_event, *args):

        data_callback   = payload_event['data']
        callback_id     = payload_event['id']
        message_id      = payload_event['message']['message_id'] # 'message': {'message_id': 1234 ()
        chat_id         = payload_event['chat_id'] # 'message': {'chat': {'id':

        self.log(payload_event)

        message_id: '{{ trigger.event.data.message.message_id }}'
        chat_id: '{{ trigger.event.data.user_id }}'


        self.call_service(
            'telegram_bot/answer_callback_query',
            message='OK',
            callback_query_id=callback_id
            )

        self.call_service(
            'telegram_bot.edit_replymarkup',
            message_id='XXXX',
            callback_query_id=callback_id,
            inline_keyboard=[]
            )
