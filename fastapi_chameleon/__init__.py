"""fastapi-chameleon - Adds integration of the Chameleon template language to FastAPI.

Entry points:

- ``global_init(template_folder, auto_reload=False, cache_init=True)``: call once at startup, before
  view modules are imported. Repeat calls are ignored unless ``cache_init=False``.
- ``@template(template_file=None, mimetype='text/html')``: decorate a FastAPI view (sync or async).
  The view returns a ``dict`` of template variables, or a ``fastapi.Response`` to bypass the template.
- ``not_found(four04template_file='errors/404.pt')`` and ``generic_error(template_file, status_code,
  template_data=None)``: raise to short-circuit a decorated view with a rendered error page.
- ``response(template_file, mimetype='text/html', status_code=200, **template_data)``: render without the
  decorator.
- ``fastapi_chameleon.exceptions``: ``FastAPIChameleonException`` (base), ``FastAPIChameleonNotFoundException``,
  ``FastAPIChameleonGenericException``.
- ``fastapi_chameleon.engine.render()`` and ``engine.clear()``: render to a string, and reset engine state
  (test isolation).

Docs: https://mkennedy.codes/docs/fastapi-chameleon/ (agents: /llms-full.txt and /skill.md).
"""

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
