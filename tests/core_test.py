from unittest import TestCase, main
from lightbot import bot

class CoreTest(TestCase):

    def setUp(self):
        r'''Тест библиотеки == тест бота
            при запуске надо будет указать токен бота, 
            затем бот будет просить сделать действие, 
            или библиотека сама будет производить действия
            для проверки работоспособности
        '''
        pass

    def test_edit_message(self):
        pass

    def test_send_message(self):
        pass

    def test_send_photo(self):
        pass

    def test_send_document(self):
        pass

    def test_download_file(self):
        pass

    def test_bind_command(self):
        pass

    def test_bind_callback(self):
        pass

    def test_bind_event(self):
        pass

    def test_bind_input(self):
        pass

    def test_unregistred_event(self):
        pass

    def test_unregistred_command(self):
        pass

    def test_get_events(self):
        pass


if __name__ == '__main__':
    main()
