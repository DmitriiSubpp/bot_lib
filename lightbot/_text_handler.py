def text_handler(bot, action):
    input = action.get('input')
    text = bot.message.text
    callback_func = bot.text_callbacks.get(text)

    if input is not None:
        callback = action.pop('input')
        callback['func']()
        return

    if callback_func is not None:
        callback_func()
        return

    callback_func = bot.update_callbacks.get('text')
    if callback_func is not None:
        callback_func()
