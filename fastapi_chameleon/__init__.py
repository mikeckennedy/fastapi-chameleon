"""fastapi-chameleon - Adds integration of the Chameleon template language to FastAPI."""

__version__ = '0.1.9'
__author__ = 'Michael Kennedy <michael@talkpython.fm>'
__all__ = ['template', 'global_init']

from .engine import global_init
from .engine import template
from .engine import response
