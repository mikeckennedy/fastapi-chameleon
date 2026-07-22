"""fastapi-chameleon - Adds integration of the Chameleon template language to FastAPI."""

from importlib.metadata import PackageNotFoundError, version

# Read the version from the installed package metadata so pyproject.toml stays the single source of truth.
try:
    __version__ = version('fastapi_chameleon')
except PackageNotFoundError:  # Running from a source tree without an installed distribution.
    __version__ = '0.0.0'

__author__ = 'Michael Kennedy <michael@talkpython.fm>'
__all__ = [
    'template',
    'global_init',
    'not_found',
    'response',
    'generic_error',
]

from .engine import generic_error
from .engine import global_init
from .engine import not_found
from .engine import response
from .engine import template
