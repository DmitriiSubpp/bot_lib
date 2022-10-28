import requests
import sys


class User:
    def __init__(self, user):
        self.id = user.get('id')
        self.is_bot = user.get('is_bot')
        self.first_name = user.get('first_name')
        self.last_name = user.get('last_name')
        self.username = user.get('username')
        self.language_code = user.get('language_code')


class Message:
    def __init__(self, message):
        self.message_id = message.get('message_id')
        self.user = message.get('from')
        self.text = message.get('text')
        self.date = message.get('date')
        self.voice = message.get('voice')


class Core:
    def __init__(self, text_handler, voice_handler):
        self.url = ''
        self.DEBUG = True

        self.text_callbacks = {}
        self.users_table = {}
        self.update_callbacks = {}

        self.handlers = {
            'text': text_handler,
            'voice': voice_handler
        }

        self.data = {'offset': 0, 'limit': 0, 'timeout': 0}
        self.message = Message({})
        self.user = User({})

    def on_text(self, text, func):
        self.text_callbacks[text] = func

    def on_update(self, update_type, func):
        self.update_callbacks[update_type] = func

    def send_message(self, text, chat_id=None, parse_mode='markdown'):
        message_data = {
            'chat_id': self.user.id if chat_id is None else chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': {}
        }
        requests.get(f'{self.url}/sendMessage', data=message_data)

        if self.DEBUG:
            print(f'DEBUG: send message to user {self.user.id}')

    def bind_input(self, message_type, func, alt=None):
        if self.user.id is None:
            if self.DEBUG:
                print('DEBUG (bind_input): user.id is None')
            return

        action = self.users_table.get(self.user.id)
        if action is not None:
            self.users_table[self.user.id]['input'] = {
                'type': message_type, 'func': func, 'alt': alt
            }

        if self.DEBUG:
            print(
                f'DEBUG (bind_input): input action type=\'{message_type}\' binded for user {self.user.id}')

    def bind_next(self, func):
        if self.user.id is None:
            if self.DEBUG:
                print('DEBUG (bind_next): user.id is None')
            return

        action = self.users_table.get(self.user.id)
        if action is not None:
            self.users_table[self.user.id]['next'] = func

        if self.DEBUG:
            print(
                f'DEBUG (bind_next): next action binded for user {self.user.id}')

    def get_update_type(self):
        if self.message.text is not None:
            return 'text'
        if self.message.voice is not None:
            return 'voice'

    def type_handler(self, type):
        action = self.users_table[self.user.id]

        next = action.get('next')
        if next is not None:
            if self.DEBUG:
                print(f'DEBUG: action: \'next\' for user {self.user.id} ')
            next = action.pop('next')
            # сообщение об удалении action
            next()
            return

        input = action.get('input')
        if input is not None:
            if self.DEBUG:
                print(
                    f'DEBUG: action exists: \'input\' of type={type} for user {self.user.id} ')
            if action['input']['type'] != type:
                if action['input']['alt'] is not None:
                    action['input']['alt']()
                return

        if action == {} and self.DEBUG:
            print(f'DEBUG: no actions binded for user {self.user.id}')

        handler = self.handlers.get(type)
        if handler is not None:
            handler(self, action)

    def get_update(self, show_update):
        updates = requests.get(f'{self.url}/getUpdates', data=self.data)
        telegram_response = updates.json()['ok']
        result = updates.json()['result']

        if telegram_response is False:
            print(f'telegram response: {updates.json()}')
            sys.exit(0)

        if len(result) == 1:
            update = result[0]
            self.data['offset'] = update['update_id'] + 1
            if show_update:
                print(update)
            return update
        return None

    def parse_message(self, update):
        self.message = Message(update['message'])
        self.user = User(self.message.user)

        if self.users_table.get(self.user.id) is None:
            self.users_table[self.user.id] = {}

    def run(self, token='', show_update=False):
        self.token = token
        self.url = f'https://api.telegram.org/bot{token}'

        while True:
            update = self.get_update(show_update)
            if update is None:
                continue

            self.parse_message(update)

            type = self.get_update_type()
            self.type_handler(type)
