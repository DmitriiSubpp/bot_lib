<p align="center">
 <img src="https://i.imgur.com/rSyq3MW.png" alt="The Documentation Compendium"></a>
</p>

<h3 align="center">The Lightbot</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/badge/license-CC0-blue.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

</div>

---

<p align = "center">💡 Документация по работе с библиотекой. (Документация в разработке)</p>


## Приступим к работе

- [Авторизация бота и запуск](#bot_init)

- [Связываем события с функциями](#bind)
  - [Связываем команды - bind_command()](#bind_command)
  - [Связываем callback кнопки - bind_callback()](#bind_callback)
  - [Связываем события целиком - bind_event()](#bind_event)
- [Обработка событий](#events)
  - [Обработка текста и команд](#text_handler)
  - [Обработка фотографий](#photo_handler)
  - [Обработка документов](#document_handler)
  - [Обработка голосовых сообщений](#voice_handler)
  - [Обработка незарегистрированных команд](#unregistred_commands)
  - [Обработка незарегистрированных событий](#unregistred_events)
- [Отправка сообщений - send_message() ](#send_message)
- [Работа с клавиатурами](#keyboards)
  - [Inline клавиатуры](#inline_keyboards)
  - [Reply клавиатуры](#reply_keyboards)
- [Ожидание события от пользователя - bind_input()](#input)
- [Скачивание файлов - download_file()](#download_files)
- [Обратная связь](#feedback)
- [Acknowledgements](#acknowledgements)


## Авторизация бота и запуск <a name = "bot_init"></a>

Чтобы авторизировать бота, достаточно передать его токен при запуске бота 
```python
from lightbot import bot
bot.run(token='55950...YoxWc')
```
Запуск:
```python
def run(show_event=False)
``` 
Метод запускает бота, он должен вызыватся самым последним.
Принимает параметр show_event. Когда True, печатает ответ от телеграма.

## Связываем события с функциями <a name = "bind"></a>

Для того чтобы добавить функционал боту, надо связать действия пользователя и функции, которые будут вызываться когда пользователь это действие совершает.
Связывание происходит глобально, это значит, что команды, кнопки и события будут доступны в любом месте диалога с ботом.
Если необходимо сделать ветвление - [вот более подходящий метод](#dialog)

### Связываем команды - bind_command() <a name = "bind_command"></a>

Для связывания текстовой команды с функцией используется метод bind_command класса Bot:
```python
def bind_command(self, command, handler, data=None):
```

В параметр command передается строка с текстом, которая будет означать команду,
В параметр handler передаётся функция, которая будет вызываться по команде,
В параметр data можно передать что-то, что далее будет передаваться в функцию

Пример без передачи переменной в параметр data
```python
from lightbot import bot
...

def start_func():
    pass
    
if __name__ == '__main__':
    bot.bind_command('/start', start_func)
    bot.run(token='55950...YoxWc')
```

Пример с передачей переменной в параметр data 
```python
from lightbot import bot
...

def start_func(data):
    print(data) # hello, world!
    
if __name__ == '__main__':
    bot.bind_command('/start', start_func, data='hello, world!')
    bot.run(token='55950...YoxWc')
```

### Связываем callback кнопки - bind_callback() <a name = "bind_callback"></a>

Для связывания callback кнопки с функцией используется метод bind_callback класса Bot:
```python
def bind_callback(self, command, handler, data=None):
```

В параметр command передается строка с текстом кнопки,
В параметр handler передаётся функция, которая будет вызываться по нажатию этой кнопки,
В параметр data можно передать что-то, что далее будет передаваться в функцию [(См. bind_command())](#bind_command).

```python
# Пример
from lightbot import bot, InlineKeyboard
...

def button_handler():
    bot.send_message('кнопка была нажата')


def start_func():
    keyboard = InlineKeyboard()
    keyboard.add_button('кнопка')
    bot.send_message("Нажми на кнопку", keyboard=keyboard.layout)
    

if __name__ == '__main__':
    bot.bind_command('/start', start_func)
    bot.bind_callback('кнопка', button_handler) # связываем кнопку и функцию, которая будет вызыватся при нажатии
    bot.run(token='55950...YoxWc')
```

### Связываем события целиком - bind_event() <a name = "bind_event"></a>

Для связывания события с функцией используется метод bind_event класса Bot:
```python
def bind_event(self, event, handler, data=None):
```

В параметр event передается строка с названием события (См. ниже),
В параметр handler передаётся функция, которая будет вызываться по возникновению этого события,
В параметр data можно передать что-то, что далее будет передаваться в функцию [(См. bind_command())](#bind_command).

Реализованы события:
- text: когда приходит текстовое сообщение
- location: когда приходит сообщение с локацией
- photo: когда приходит фотография
- document: когда приходит документ
- voice: когда приходит голосовое сообщение

[Как правильно обрабатывать события](#events)

```python
# Пример
from lightbot import bot
...

def photo_handler():
    bot.send_message("Получена фотография")
    
    
if __name__ == '__main__':
    bot.bind_event('photo', photo_handler)
    bot.run(token='55950...YoxWc')
```


## Обработка событий <a name = "events"></a>

При возникновении события (например пользователь отправил фотографию) библиотека парсит данные, которые пришли от телеграма и заполняет свои переменные.
Далее будет написано, какие переменные заполняются при конкретном событии и как к ним можно обратиться.

### Обработка текста и команд <a name="text_handler"></a>

Когда пользователь отправляет простой текст или команду (она интерпретируется как простой текст), библиотека парсит его и текст пользователя можно получить через переменную text класса Bot:

```python
# пример эхо-бота
from lightbot import bot

def on_text():
    text = bot.text
    bot.send_message(text)
    

if __name__ == '__main__':
    bot.bind_event('text', on_text)
    bot.run(token='55950...YoxWc')
```

### Обработка фотографий <a name="photo_handler"></a>

Если пользователь отправляет фотографию, её данные можно получить через переменную photo класса Bot:

```python
# пример
from lightbot import bot

def on_photo():
    print(bot.photo)
    

if __name__ == '__main__':
    bot.bind_event('photo', on_photo)
    bot.run(token='55950...YoxWc')
```

Переменная photo содержит список со словарями.

### Обработка документов <a name="document_handler"></a>

Если пользователь отправляет документ, его данные можно получить через переменную document класса Bot:

```python
# пример
from lightbot import bot

def on_document():
    print(bot.document)
    

if __name__ == '__main__':
    bot.bind_event('document', on_document)
    bot.run(token='55950...YoxWc')
```

### Обработка голосовых сообщений <a name="voice_handler"></a>

Если пользователь отправляет голосовое сообщение, его данные можно получить через переменную voice класса Bot:

```python
# пример
from lightbot import bot

def on_voice():
    print(bot.voice)
    

if __name__ == '__main__':
    bot.bind_event('voice', on_document)
    bot.run(token='55950...YoxWc')
```

### Обработка незарегистрированных команд <a name="unregistred_commands"></a>

Если пользователь отправляет команду или текст, который не связан ни с какой функцией, то можно отловить этот текст при помощи метода unregistred_command класса Bot:

```python
def unregistred_command(self, handler):
```
handler - это функция, которая вызывается если на полученный текст н еназначен обработчик

```python
# пример
from lightbot import bot

def on_start():
    pass
    

def unregistred():
    bot.send_message('такой команды нет')


if __name__ == '__main__':
    bot.bind_command('/start', on_start)
    bot.unregistred_command(unregistred)
    bot.run(token='55950...YoxWc')
```
Функция unregistred будет вызыватся всякий раз, когда текст не является командой '/start'

### Обработка незарегистрированных событий <a name="unregistred_events"></a>

Если пользователь отправляет команду или текст, который не связан ни с какой функцией, то можно отловить этот текст при помощи метода unregistred_event класса Bot:

```python
def unregistred_command(self, handler):
```
handler - это функция, которая вызовется, если на событие не назначен обработчик.

```python
# пример
from lightbot import bot

def on_document():
    bot.send_message('Прислан документ')
    

def unregistred():
    bot.send_message('такого события нет')


if __name__ == '__main__':
    bot.bind_event('document', on_document)
    bot.unregistred_event(unregistred)
    bot.run(token='55950...YoxWc')
```
функция unregistred будет вызыватся всякий раз, когда присылается не документ


## Отправка сообщений - send_message() <a name = "send_message"></a>

Для отправки сообщений используется метод send_message класса Bot:
```python
def send_message(text, keyboard={}, ...):
```

к сообщению можно прикрепить клавиатуру, достаточно передать в параметр keyboard объект класса InlineKeyboard или ReplyKeyboard ([Подробнее о кравиатурах](#keyboards))

```python
from lightbot import bot
...

def some_func():
    bot.send_message("hello, world!"):
```

## Работа с клавиатурами <a name = "keyboards"></a>

### Inline клавиатуры <a name="inline_keyboards"></a>

```python
from lightbot import bot, InlineKeyboard
...

def some_func():
    keyboard = InlineKeyboard()
    keyboard.add_buttons('btn1', 'btn2')
    keyboard.add_buttons('btn3')
    bot.send_message("hello, world", keyboard=keyboard.layout)
    
```
### Reply клавиатуры <a name="reply_keyboards"></a>

```python
from lightbot import bot, ReplyKeyboard
...

def some_func():
    keyboard = ReplyKeyboard(one_time_keyboard=True)
    keyboard.add_buttons('btn1', 'btn2')
    keyboard.add_buttons('btn3')

    bot.send_message("hello, world", keyboard=keyboard.layout)
```
    
## Ожидание события от пользователя - bind_input() <a name="input"></a>

Ожидание события - бот ждет, когда пользователь сделать определенное действие, так можно сделать ветвление, или сделать запрос на фотографию.

```python
def bind_input(self, event, handler, cancel_command=None):
```

Ожидание события:
- text
- location
- photo
- document
- voice

Если задано ожидание от пользователя конкретного события, то никакое другое событие не будет обрабатываться. Бот будет ждать только заданное событие.

```python
from lightbot import bot
...

def some_func():
    bot.send_message("Отправь мне фотографию")
    bot.bind_input('photo', process_photo)
    

def process_photo():
    # Обработка полученной фотографии
    pass
```

Можно задать команду отмены ожидания текста, для этого надо заранее забиндить команду отмены на функцию:

```python
from lightbot import bot
...

def some_func():
    keyboard = ReplyKeyboard(one_time_keyboard=True)
    keyboard.add_buttons('Отмена')
       
    bot.send_message("Отправь мне текст", keyboard=keyboard.layout)
    
    bot.bind_command('отмена', cancel_func)
    bot.bind_input('text', process_text, cancel_command='отмена')


def process_text():
    # Обработка полученной фотографии
    pass
    
    
def cancel_func():
    bot.send_message("Ожидание отменено")
```

## Скачивание файлов - download_file() <a name="download"></a>

Скачивание файлов происходит через метод download_file класса Bot:
```python
def download_file(self, file_id, path=None):
```
- file_id для фотографий: 
  - bot.photo[2]['file_id'] - фотография лучшего качества
  - bot.photo[1]['file_id'] - фотография сруднего качества
  - bot.photo[0]['file_id'] - фотография худшего качества
- file_id для документов: bot.document['file_id']
- file_id для голосовых сообщений: bot.voice['file_id']

Путь сохранения файлов по умолчанию:
- голосовые сообщения скачиваются в папку voice
- документы скачиваются в папку documents
- фотографии скачиваются в папку photos

Свой путь можно задать через параметр path

```python
# пример
from lightbot import bot
...


def on_document():
    file_id = bot.photo[2]['file_id'] # лучшее качество фотографии
    bot.download_file(file_id) # фотография будет сохранена в папку /photos


if __name__ == '__main__':
    bot.bind_event('photo', on_photo)
    bot.run()
```

## Обратная связь <a name = "feedback"></a>

- [feedmereadmes]([https://github.com/LappleApple/feedmereadmes](https://github.com/DmitriiSubpp)) - мои контакты


## Acknowledgements <a name = "acknowledgements"></a>

1. [Documenting your projects on GitHub](https://guides.github.com/features/wikis/) - GitHub Guides
2. [documentation-handbook](https://github.com/jamiebuilds/documentation-handbook) - jamiebuilds
3. [Documentation Guide](https://www.writethedocs.org/guide/) - Write the Docs


## P.S. <a name = "ps"></a>

- Этот репозиторий находится в активной разработке. Если у тебя есть предложения по улучшению, пожалуйста, воспользуйся [issue](#) или пришли свой [Pull Request](#)
