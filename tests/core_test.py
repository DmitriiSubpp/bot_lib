from unittest import TestCase, main
from ..lightbot import bot


class CoreTest(TestCase):

    def setUp(self):
        self.test = ''

        bot.text_callbacks = {}
        bot.users_table = {}
        bot.update_callbacks = {}

        self.message_text = {
            'update_id': 635741487,
            'message': {
                'message_id': 3782,
                'from': {
                    'id': 476210966,
                    'is_bot': False,
                    'first_name': 'Дмитрий',
                    'last_name': 'Орешкин',
                    'username': 'dmitriisub',
                    'language_code': 'en'
                },
                'chat': {
                    'id': 476210966,
                    'first_name': 'Дмитрий',
                    'last_name': 'Орешкин',
                    'username': 'dmitriisub',
                    'type': 'private'
                },
                'date': 1666465072,
                'text': 'sample_text'
            }
        }

        self.message_voice = {
            'update_id': 635741487,
            'message': {
                'message_id': 3782,
                'from': {
                    'id': 476210967,
                    'is_bot': False,
                    'first_name': 'Дмитрий',
                    'last_name': 'Орешкин',
                    'username': 'dmitriisub',
                    'language_code': 'en'
                },
                'chat': {
                    'id': 476210967,
                    'first_name': 'Дмитрий',
                    'last_name': 'Орешкин',
                    'username': 'dmitriisub',
                    'type': 'private'
                },
                'date': 1666465072,
                'voice': {
                    'duration': 1,
                    'mime_type': 'audio/ogg',
                    'file_id': 'AwA..GoE',
                    'file_unique_id': 'AgADYCIAAijMqEo',
                    'file_size': 4992
                }
            }
        }

    def test_get_update_type(self):
        bot.parse_message(self.message_text)
        self.assertEqual(bot.get_update_type(), 'text')

        bot.parse_message(self.message_voice)
        self.assertEqual(bot.get_update_type(), 'voice')

    def test_on_text(self):
        def testf():
            self.test = 'pass'

        bot.parse_message(self.message_text)
        bot.on_text('sample_text', testf)
        bot.type_handler('text')

        self.assertEqual(self.test, 'pass')
        self.assertEqual(bot.text_callbacks, {'sample_text': testf})

    def test_on_update_voice(self):
        def testf():
            self.test = 'pass'

        bot.parse_message(self.message_voice)
        bot.on_update('voice', testf)
        bot.type_handler('voice')

        self.assertEqual(self.test, 'pass')
        self.assertEqual(bot.update_callbacks, {'voice': testf})

    def test_on_update_text(self):
        def testf():
            self.test = 'pass'

        bot.parse_message(self.message_text)
        bot.on_update('text', testf)
        bot.type_handler('text')

        self.assertEqual(self.test, 'pass')
        self.assertEqual(bot.update_callbacks, {'text': testf})

    def test_on_update(self):
        def testf():
            return True

        bot.parse_message(self.message_text)
        bot.on_update('text', testf)

        bot.parse_message(self.message_voice)
        bot.on_update('voice', testf)

        self.assertEqual(bot.update_callbacks, {'text': testf, 'voice': testf})


if __name__ == '__main__':
    main()
