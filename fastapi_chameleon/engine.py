import inspect
import os
from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Optional, Union, overload

import fastapi
from chameleon import PageTemplateLoader, PageTemplate

from fastapi_chameleon.exceptions import (
    FastAPIChameleonException,
    FastAPIChameleonGenericException,
    FastAPIChameleonNotFoundException,
)

__templates: Optional[PageTemplateLoader] = None
template_path: Optional[str] = None

P = ParamSpec('P')
R = TypeVar('R')


# Overload for when the decorator is used with arguments.
@overload
def template(
        template_file: Optional[Union[Callable[..., R], str]] = None,
        mimetype: str = 'text/html'
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    ...


# Overload for when the decorator is used without arguments.
@overload
def template(
        f: Callable[P, R]
) -> Callable[P, R]:
    ...


def global_init(template_folder: str, auto_reload=False, cache_init=True):
    global __templates, template_path

    if __templates and cache_init:
        return

    if not template_folder:
        msg = 'The template_folder must be specified.'
        raise FastAPIChameleonException(msg)

    if not os.path.isdir(template_folder):
        msg = f"The specified template folder must be a folder, it's not: {template_folder}"
        raise FastAPIChameleonException(msg)

    template_path = template_folder
    __templates = PageTemplateLoader(template_folder, auto_reload=auto_reload)


def clear():
    global __templates, template_path
    __templates = None
    template_path = None


def render(template_file: str, **template_data: dict) -> str:
    if not __templates:
        raise FastAPIChameleonException('You must call global_init() before rendering templates.')

    page: PageTemplate = __templates[template_file]
    return page.render(encoding='utf-8', **template_data)


def response(template_file: str, mimetype='text/html', status_code=200, **template_data) -> fastapi.Response:
    html = render(template_file, **template_data)
    return fastapi.Response(content=html, media_type=mimetype, status_code=status_code)


def template(template_file: Optional[Union[Callable[..., R], str]] = None, mimetype: str = 'text/html'):
    """
    Decorate a FastAPI view method to render an HTML response.

    :param str template_file: Optional, the Chameleon template file (path relative to template folder, *.pt).
    :param str mimetype: The mimetype response (defaults to text/html).
    :return: Decorator to be consumed by FastAPI
    """
    if callable(template_file):
        # If the first parameter is callable, the decorator is being used without arguments.
        func = template_file
        template_file = None
        return _decorate(func, template_file, mimetype)
    else:
        # If template_file is not callable, return a lambda that will wrap the function.
        return lambda f: _decorate(f, template_file, mimetype)


def _decorate(f: Callable[P, R], template_file: Optional[str], mimetype: str) -> Callable[P, R]:
    """
    Internal decorator function that wraps the FastAPI view function to handle rendering.
    It supports both synchronous and asynchronous view methods.

    :param f: The original FastAPI view function.
    :param template_file: The optional template file path. If None, a default naming scheme is applied.
    :param mimetype: The mimetype for the response.
    :return: The wrapped function with additional rendering logic.
    """
    global template_path

    # Ensure the global template_path is initialized; default to 'templates' if not set.
    if not template_path:
        template_path = 'templates'
        # Optionally, raise an exception if template_path must be initialized beforehand:
        # raise FastAPIChameleonException("Cannot continue: fastapi_chameleon.global_init() has not been called.")

    # If no template file was provided, derive it from the function's module and name.
    if not template_file:
        # Use the default naming scheme: template_folder/module_name/function_name.pt
        module = f.__module__

        # Use only the last part of the module name if it's a dotted path.
        if '.' in module:
            module = module.split('.')[-1]
        view = f.__name__

        # Default to an HTML template
        template_file = f'{module}/{view}.html'

        # If the .html file does not exist, fallback to a .pt template.
        if not os.path.exists(os.path.join(template_path, template_file)):
            template_file = f'{module}/{view}.pt'

    @wraps(f)
    def sync_view_method(*args: P.args, **kwargs: P.kwargs) -> R:
        """
        Synchronous wrapper for the view function.
        Calls the view, renders the response using the specified template,
        and handles exceptions by rendering error templates.
        """
        try:
            response_val = f(*args, **kwargs)
            return __render_response(template_file, response_val, mimetype)
        except FastAPIChameleonNotFoundException as nfe:
            return __render_response(nfe.template_file, {}, 'text/html', 404)
        except FastAPIChameleonGenericException as nfe:
            template_data = nfe.template_data if nfe.template_data is not None else {}
            return __render_response(nfe.template_file, template_data, 'text/html', nfe.status_code)

    @wraps(f)
    async def async_view_method(*args: P.args, **kwargs: P.kwargs) -> R:
        """
        Asynchronous wrapper for the view function.
        Awaits the view, renders the response using the specified template,
        and handles exceptions by rendering error templates.
        """
        try:
            response_val = await f(*args, **kwargs)
            return __render_response(template_file, response_val, mimetype)
        except FastAPIChameleonNotFoundException as nfe:
            return __render_response(nfe.template_file, {}, 'text/html', 404)
        except FastAPIChameleonGenericException as nfe:
            template_data = nfe.template_data if nfe.template_data is not None else {}
            return __render_response(nfe.template_file, template_data, 'text/html', nfe.status_code)

    # Return the appropriate wrapper based on whether the original function is a coroutine.
    if inspect.iscoroutinefunction(f):
        return async_view_method
    else:
        return sync_view_method


def __render_response(template_file, response_val, mimetype, status_code: int = 200) -> fastapi.Response:
    # source skip: assign-if-exp
    if isinstance(response_val, fastapi.Response):
        return response_val

    if template_file and not isinstance(response_val, dict):
        msg = f'Invalid return type {type(response_val)}, we expected a dict or fastapi.Response as the return value.'
        raise FastAPIChameleonException(msg)

    model = response_val

    html = render(template_file, **model)
    return fastapi.Response(content=html, media_type=mimetype, status_code=status_code)


def not_found(four04template_file: str = 'errors/404.pt'):
    msg = 'The URL resulted in a 404 response.'

    if four04template_file and four04template_file.strip():
        raise FastAPIChameleonNotFoundException(msg, four04template_file)
    else:
        raise FastAPIChameleonNotFoundException(msg)


def generic_error(template_file: str, status_code: int, template_data: Optional[dict] = None):
    msg = 'The URL resulted in an error.'

    raise FastAPIChameleonGenericException(template_file, status_code, msg, template_data=template_data)
