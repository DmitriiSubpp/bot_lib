def voice_handler(bot, action):
    input = action.get('input')
    if input is not None:
        callback = action.pop('input')
        callback['func']()
        return

    callback_func = bot.update_callbacks.get('voice')
    if callback_func is not None:
        callback_func()
