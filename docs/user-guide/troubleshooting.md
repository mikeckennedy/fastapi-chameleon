# Troubleshooting

It is late, the deploy just went out, and the Shelf Life home page is a white screen with `Internal Server Error` on it. The server log, happily, knows exactly what happened. This page is the field guide for reading it.

Every error you can meet falls into one of three groups. Errors the package raises itself are [FastAPIChameleonException](../reference/exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException) or a subclass, and their messages are written to be read by a human. Errors from Chameleon while compiling or rendering a template arrive as `ValueError`, `NameError`, `AttributeError`, or one of Chameleon's own types, and they name the file, the variable, or the expression that failed. And then there is behaviour that is working exactly as designed and still looks like a bug until you know the rule. All three groups surface as a `500` in the browser and a traceback in the log, so always start from the log.


# Errors from the package


## `FastAPIChameleonException: You must call global_init() before rendering templates.`

A decorated view, [response()](../reference/response.md#fastapi_chameleon.response), or `engine.render()` ran before [global_init()](../reference/global_init.md#fastapi_chameleon.global_init). The engine has no template folder and nothing to load from. Call `global_init(template_folder)` once at startup, in the module that creates the app, before requests are served. In tests, use a fixture that calls it and clears the engine afterwards. See [Testing and CI](testing.md).


## `FastAPIChameleonException: The template_folder must be specified.`

[global_init()](../reference/global_init.md#fastapi_chameleon.global_init) was called with an empty string or `None`. Usually a settings value that did not load. Pass the path to your templates folder.


## `FastAPIChameleonException: The specified template folder must be a folder, it's not: ...`

The path does not exist or points at a file. The message shows the path exactly as the package saw it, which is the clue: relative paths resolve against the current working directory, and that directory differs between `python main.py`, `uvicorn main:app`, your test runner, and your container. Build the path from `__file__` instead and the problem disappears for good:

``` python
BASE_DIR = Path(__file__).resolve().parent
fastapi_chameleon.global_init(BASE_DIR / 'templates')
```


## `FastAPIChameleonException: Invalid return type <class 'NoneType'>, we expected a dict or fastapi.Response as the return value.`

The view returned something other than a `dict` or a `fastapi.Response`. `NoneType` almost always means a missing `return` statement. Any other type means a model object, a list, or a string came back from the data layer and was passed straight through. Convert it: `model.model_dump()` for Pydantic, `dataclasses.asdict(obj)` for dataclasses, `{'items': items}` for a list.


## `500 Internal Server Error`, log shows `FastAPIChameleonNotFoundException: The URL resulted in a 404 response.`

[not_found()](../reference/not_found.md#fastapi_chameleon.not_found) was called from code that is not below a `@template`-decorated view. The same applies to `FastAPIChameleonGenericException: The URL resulted in an error.` from [generic_error()](../reference/generic_error.md#fastapi_chameleon.generic_error). The function raised as designed, but nothing above it was listening, so FastAPI treated it as a crash. Decorate the route, or raise `fastapi.HTTPException(status_code=404)` from undecorated code. See [Friendly Error Pages](error-pages.md).


## `TypeError: 'PosixPath' object is not iterable` inside `chameleon/loader.py`

Versions up to 0.1.18 accepted a `pathlib.Path` in [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) without complaint, then handed it to Chameleon's loader, which tried to iterate it as a list of search paths. Upgrade, or wrap the path in `str()`. Current versions accept any `os.PathLike`.


# Errors from Chameleon


## `ValueError: Template not found: home/missing.pt.`

The template path does not exist under the folder given to [global_init()](../reference/global_init.md#fastapi_chameleon.global_init). The path in the message is relative to that folder, so check for a typo, a wrong subfolder, or `.html` versus `.pt`. If the view uses the bare `@template` form, the expected path is `{module}/{function}.html` or `.pt`, where `module` is the last segment of the view's module name: a view named `index` in `views/home.py` wants `home/index.pt`. If the path looks right and the file is definitely there, the engine is probably pointing at the wrong folder because [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) ran after the view module was imported. See [Decorating Views](views.md).


## `NameError: items`

The template referenced a variable the view did not return. Chameleon names the missing variable for you. Add it to the dict the view returns, or guard the element with `tal:condition`. The same error appears when a shared layout uses a variable, such as `title`, that one of its pages forgot to provide.


## `AttributeError: 'NoneType' object has no attribute 'upper'`

An expression inside `${ }` or a `tal:` attribute failed partway through. Chameleon appends the expression that failed, for example `- Expression: "title.upper()"`, so you know exactly which line of the template to look at. Fix the data the view returns, or make the expression tolerate the value.


## `chameleon.exc.LanguageError` or `chameleon.exc.ExpressionError`

The template itself has a bug: an invalid `tal:` attribute such as `tal:repeat="x"` without a sequence to repeat over, or a Python expression with a syntax error. These are raised the first time the template is compiled, which is the first request that uses it, so a template nobody has visited since the last edit can carry a broken expression into production unnoticed. The message includes the offending string and the file name.


# Behaviour that looks like a bug


## Template edits are not showing up

You edited the template, refreshed, and nothing changed. Templates are compiled once and cached. Pass `auto_reload=True` to [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) during development. If you already did and it still happens, check whether [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) is being called twice: the second call is ignored unless `cache_init=False`, so the first call's settings win. See [Configuration](configuration.md).


## The wrong template renders, or the bare `@template` form cannot find a file that exists

Template name inference runs when the view module is imported, using whatever folder is configured at that moment. If [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) had not run yet, the folder defaulted to `templates` relative to the current working directory, and a later [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) did not go back and re-resolve the name. Move [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) above the view imports, or name the template explicitly.


## My 404 page returns JSON

The request never reached a decorated view. No route matched, so FastAPI's router answered on its own, in JSON. Add a catch-all route decorated with `@template` that calls [not_found()](../reference/not_found.md#fastapi_chameleon.not_found), or register a FastAPI exception handler for `404` that returns `fastapi_chameleon.response('errors/404.pt', status_code=404)`.


## The error page itself fails with a `500`

The error template is missing or broken. [not_found()](../reference/not_found.md#fastapi_chameleon.not_found) renders `errors/404.pt` by default, so create that file. A `ValueError: Template not found: errors/404.pt.` in the log confirms this cause.


# Fix order

Work from the outside in. First make sure [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) runs once, first, with an absolute path. Then check that the view returns a dict. Then check the template path. Only then read Chameleon's message for the variable or expression it names. Nine times out of ten the problem is in the first two steps, and the log told you so in the first line.
