import inspect
import os
from functools import wraps
from typing import Any, Awaitable, Callable, NoReturn, Optional, ParamSpec, TypeVar, Union, cast, overload

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
    template_file: Optional[Union[Callable[..., R], str]] = None, mimetype: str = 'text/html'
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


# Overload for when the decorator is used without arguments.
@overload
def template(f: Callable[P, R]) -> Callable[P, R]: ...


def global_init(template_folder: str, auto_reload: bool = False, cache_init: bool = True) -> None:
    """
    Initialize the Chameleon template engine for your app.

    Call this once at startup, pointing it at the folder that holds your ``*.pt``
    templates. Template paths used elsewhere (in ``template()``, ``response()``,
    ``not_found()``, and ``generic_error()``) are resolved relative to this folder.

    :param str template_folder: Path to the folder containing your Chameleon templates.
    :param bool auto_reload: Reload templates from disk when they change. Handy in
        development; leave ``False`` in production. Defaults to ``False``.
    :param bool cache_init: When ``True`` (the default), a second call is a no-op once
        the engine is already initialized. Pass ``False`` to force re-initialization
        (for example, to switch template folders in tests).
    :raises FastAPIChameleonException: If ``template_folder`` is empty or is not a directory.
    """
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


def clear() -> None:
    """
    Reset the engine: clear the cached template loader and template path.

    Primarily a test-isolation hook -- call it between tests (or before a fresh
    ``global_init()``) so engine state does not leak across them.
    """
    global __templates, template_path
    __templates = None
    template_path = None


def render(template_file: str, **template_data) -> str:
    """
    Render a template to a string using the configured engine.

    :param str template_file: The Chameleon template file to render (path relative to
        the template folder).
    :param template_data: Keyword arguments passed to the template as variables.
    :return: The rendered template as a UTF-8 string.
    :raises FastAPIChameleonException: If ``global_init()`` has not been called.
    """
    if not __templates:
        raise FastAPIChameleonException('You must call global_init() before rendering templates.')

    page: PageTemplate = __templates[template_file]
    return page.render(encoding='utf-8', **template_data)


def response(
    template_file: str, mimetype: str = 'text/html', status_code: int = 200, **template_data
) -> fastapi.Response:
    """
    Render a template and return it as a FastAPI response directly.

    Use this when you want a rendered ``Response`` without the ``template()``
    decorator, for example to return a fully-formed response from a view that does
    its own branching. Requires ``global_init()`` to have been called first.

    :param str template_file: The Chameleon template file to render (path relative to
        the template folder, ``*.pt``).
    :param str mimetype: The response media type. Defaults to ``text/html``.
    :param int status_code: The HTTP status code for the response. Defaults to ``200``.
    :param template_data: Keyword arguments passed through to the template as variables.
    :return: A ``fastapi.Response`` containing the rendered template, with the given
        media type and status code.
    :raises FastAPIChameleonException: If ``global_init()`` has not been called.
    """
    html = render(template_file, **template_data)
    return fastapi.Response(content=html, media_type=mimetype, status_code=status_code)


def template(template_file: Optional[Union[Callable[..., R], str]] = None, mimetype: str = 'text/html'):
    """
    Decorate a FastAPI view to render its return value through a Chameleon template.

    Works on both sync and async view functions, and can be used three ways::

        @template('home/index.pt')   # explicit template file
        @template()                  # infer the template name
        @template                    # bare form, also infers the name

    When no template file is given, the name is inferred as ``{module}/{function}``
    under the template folder (the module's last dotted segment and the view's name),
    preferring a ``.html`` file and falling back to ``.pt``.

    The decorated view should return a ``dict`` (used as the template's variables). If
    it returns a ``fastapi.Response`` instead, the template is skipped and the response
    is passed through unchanged. Returning anything else raises
    ``FastAPIChameleonException``.

    :param template_file: The Chameleon template file (path relative to the template
        folder). Omit it (or pass ``None``) to infer the name from the view. In the bare
        ``@template`` form this argument receives the view function itself.
    :param str mimetype: The response media type. Defaults to ``text/html``.
    :return: The decorated view (bare form) or a decorator to apply to the view.
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
        # getattr (not f.__name__) so type checkers don't flag __name__ on the generic Callable[P, R].
        view = getattr(f, '__name__')

        # Default to an HTML template
        template_file = f'{module}/{view}.html'

        # If the .html file does not exist, fallback to a .pt template.
        if not os.path.exists(os.path.join(template_path, template_file)):
            template_file = f'{module}/{view}.pt'

    @wraps(f)
    def sync_view_method(*args: P.args, **kwargs: P.kwargs) -> fastapi.Response:
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
    async def async_view_method(*args: P.args, **kwargs: P.kwargs) -> fastapi.Response:
        """
        Asynchronous wrapper for the view function.
        Awaits the view, renders the response using the specified template,
        and handles exceptions by rendering error templates.
        """
        try:
            response_val = await cast(Awaitable[Any], f(*args, **kwargs))
            return __render_response(template_file, response_val, mimetype)
        except FastAPIChameleonNotFoundException as nfe:
            return __render_response(nfe.template_file, {}, 'text/html', 404)
        except FastAPIChameleonGenericException as nfe:
            template_data = nfe.template_data if nfe.template_data is not None else {}
            return __render_response(nfe.template_file, template_data, 'text/html', nfe.status_code)

    # Return the appropriate wrapper based on whether the original function is a coroutine.
    # The wrappers return a fastapi.Response at runtime; we cast back to the view's declared
    # Callable[P, R] so the decorator stays signature-transparent for callers (FastAPI, type checkers).
    if inspect.iscoroutinefunction(f):
        return cast(Callable[P, R], async_view_method)
    else:
        return cast(Callable[P, R], sync_view_method)


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


def not_found(four04template_file: str = 'errors/404.pt') -> NoReturn:
    """
    Short-circuit the current view and render a friendly 404 page.

    Call this from inside a ``template()``-decorated view when a resource cannot be
    found. It raises an exception that the decorator catches and turns into an HTTP
    404 response rendered from ``four04template_file``. This function never returns
    normally.

    :param str four04template_file: The template to render for the 404 response (path
        relative to the template folder). Defaults to ``errors/404.pt``.
    :raises FastAPIChameleonNotFoundException: Always; this is how the 404 is signalled
        to the decorator.
    """
    msg = 'The URL resulted in a 404 response.'

    if four04template_file and four04template_file.strip():
        raise FastAPIChameleonNotFoundException(msg, four04template_file)
    else:
        raise FastAPIChameleonNotFoundException(msg)


def generic_error(template_file: str, status_code: int, template_data: Optional[dict] = None) -> NoReturn:
    """
    Short-circuit the current view and render an error page with a custom status code.

    Like ``not_found()``, but for any error: call it from inside a
    ``template()``-decorated view to render ``template_file`` with the HTTP
    ``status_code`` you choose (for example ``401`` or ``500``). The decorator catches
    the raised exception and builds the response. This function never returns normally.

    :param str template_file: The error template to render (path relative to the
        template folder).
    :param int status_code: The HTTP status code to return (for example
        ``fastapi.status.HTTP_401_UNAUTHORIZED``).
    :param dict template_data: Optional variables passed to the template. Defaults to
        ``None`` (an empty context).
    :raises FastAPIChameleonGenericException: Always; this is how the error is signalled
        to the decorator.
    """
    msg = 'The URL resulted in an error.'

    raise FastAPIChameleonGenericException(template_file, status_code, msg, template_data=template_data)
