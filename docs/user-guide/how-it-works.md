# How It Works

The whole library is three small modules. Knowing what happens at import time versus request time explains every gotcha in the other pages.


# Module-global engine state

[global_init()](../reference/global_init.md#fastapi_chameleon.global_init) stores two module-level values in `fastapi_chameleon.engine`: a Chameleon `PageTemplateLoader` and the template folder path. Every render goes through that one loader. There is one engine per process, which is why [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) is called once and why tests clear it between runs with `engine.clear()`.


# Decoration time

`@template(...)` runs when the view module is imported. At that moment it decides three things:

1.  **Which template.** An explicit name is kept as-is. A missing name is derived from the view's module and function name, and the `.html` or `.pt` choice is made by checking the filesystem once.
2.  **Sync or async.** `inspect.iscoroutinefunction` picks a synchronous or asynchronous wrapper. The wrapper calls or awaits the view, then renders.
3.  **The signature.** The wrapper is wrapped with `functools.wraps`, and [template()](../reference/template.md#fastapi_chameleon.template) is typed with ParamSpec-based overloads, so FastAPI's dependency injection and type checkers see the original parameters.

Because the template folder is read at decoration time for name inference, [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) has to run before the view module is imported. If it has not, the folder defaults to `templates` relative to the current working directory.


# Request time

The wrapper calls the view and looks at the return value:

- A `fastapi.Response` is returned as-is.
- A `dict` is passed to the loader as the template model and the HTML comes back in a `fastapi.Response` with the decorator's `mimetype` and status `200`.
- Anything else raises [FastAPIChameleonException](../reference/exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException).

Rendering before [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) has run raises [FastAPIChameleonException](../reference/exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException) too. A template file that does not exist raises `ValueError` from Chameleon's loader.


# Error pages are exceptions

[not_found()](../reference/not_found.md#fastapi_chameleon.not_found) and [generic_error()](../reference/generic_error.md#fastapi_chameleon.generic_error) do not return. They raise [FastAPIChameleonNotFoundException](../reference/exceptions.FastAPIChameleonNotFoundException.md#fastapi_chameleon.exceptions.FastAPIChameleonNotFoundException) or [FastAPIChameleonGenericException](../reference/exceptions.FastAPIChameleonGenericException.md#fastapi_chameleon.exceptions.FastAPIChameleonGenericException), both subclasses of [FastAPIChameleonException](../reference/exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException). The wrapper catches exactly those two types and renders the error template with the status carried by the exception, always as `text/html`. Any other exception propagates to FastAPI as usual.

This is why the functions work from anywhere below a decorated view, and why they do nothing useful outside one.


# Template caching

Chameleon compiles each template to a Python module on first use and keeps it in memory. With `auto_reload=False` that compiled version is used for the rest of the process. With `auto_reload=True` the loader checks the file's modification time before each use and recompiles when it changed.


# Source

The code is short and readable: [engine.py](https://github.com/mikeckennedy/fastapi-chameleon/blob/main/fastapi_chameleon/engine.py) and [exceptions.py](https://github.com/mikeckennedy/fastapi-chameleon/blob/main/fastapi_chameleon/exceptions.py).
