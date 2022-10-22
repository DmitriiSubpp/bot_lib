"""
The lightbot library provides interface to facilitate dealing with telegram-api in Python.
Just 'from lightbot import bot'.
"""

from ._lightbot import Core

from ._text_handler import text_handler
from ._voice_handler import voice_handler

__version__ = "0.1.0"
#__all__ = ["bot"]

bot = Core(
    text_handler=text_handler,
    voice_handler=voice_handler,
)
