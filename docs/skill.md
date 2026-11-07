---
name: fastapi-chameleon
description: Server-rendered HTML for FastAPI using the Chameleon template language. One global_init() call plus a @template decorator turns a view that returns a dict into a rendered text/html response, and not_found() and generic_error() replace FastAPI's JSON errors with HTML pages. Use when adding fastapi-chameleon to a FastAPI app, writing or editing .pt or .html Chameleon templates (TAL, METAL, ${} syntax, not Jinja), wiring global_init() and import order, returning redirects from page views, building friendly 404 or error pages, testing decorated views with pytest, or when FastAPIChameleonException, "You must call global_init()", "Invalid return type", "Template not found", or a 500 after calling not_found() appears.
license: MIT
compatibility: Python 3.10+, FastAPI, Chameleon. No environment variables, no CLI.
---

# fastapi-chameleon

FastAPI returns JSON by default. fastapi-chameleon renders Chameleon templates instead: call `global_init(template_folder)` once at startup, decorate views with `@fastapi_chameleon.template(...)`, return a `dict`, and the view hands FastAPI a `fastapi.Response` with `text/html`. Package errors are `FastAPIChameleonException` or a subclass. Template errors come from Chameleon as `ValueError`, `NameError`, or `chameleon.exc.*`.

## Install

`uv add fastapi-chameleon` or `pip install fastapi-chameleon`.

## Use

```python
from pathlib import Path
import fastapi
import fastapi_chameleon

app = fastapi.FastAPI()
fastapi_chameleon.global_init(Path(__file__).resolve().parent / 'templates', auto_reload=dev_mode)  # before view modules are imported

@app.get('/')                                   # route decorator outermost
@fastapi_chameleon.template('home/index.pt')    # path relative to the template folder
def index():
    return {'title': 'Home'}                    # dict == template variables; a fastapi.Response is passed through
```

Test form: call the view directly, `resp = index()` or `asyncio.run(index())`, and assert on `resp.status_code` and `resp.body`. Use a fixture that calls `global_init()` and `fastapi_chameleon.engine.clear()` on teardown. CI is `pytest` per interpreter, no extras.

## Rules

- `global_init()` runs once. A second call is ignored unless `cache_init=False` or `engine.clear()` was called first, so you cannot change `auto_reload` by calling it again.
- Call `global_init()` before importing view modules. Bare `@template` infers `{module}/{function}.html` then `.pt` at import time, and if the engine is not initialised yet the folder silently defaults to `templates` under the current working directory and is never re-resolved.
- Views return a `dict` or a `fastapi.Response`. Anything else, including `None` and Pydantic models, raises `FastAPIChameleonException` at request time. Use `model.model_dump()`.
- Returning any `fastapi.Response` skips the template. That is how redirects work from page views.
- `not_found()` and `generic_error()` always raise. They only work below a `@template`-decorated view. From an undecorated route, a dependency, or middleware they become a plain 500; raise `fastapi.HTTPException` there instead.
- `not_found()` renders `errors/404.pt` with an empty model. Only `generic_error()` accepts `template_data`.
- Error pages are always `text/html` at their own status. The decorator's `mimetype` does not apply to them.
- The decorator has no `status_code` parameter. A rendered dict is always 200. Use `response(...)` for other codes.
- Templates are TAL, not Jinja. `${expr}` interpolates and is escaped, `tal:repeat`, `tal:condition`, `tal:content`, `tal:attributes` control flow, `metal:use-macro="load: ../shared/layout.pt"` with `metal:fill-slot` does layouts. There is no `{% %}` or `{{ }}`.
- `.pt` and `.html` are treated identically by Chameleon. Inference prefers `.html`.
- Dependency injection keeps working on decorated views, sync or async. Path and query parameters, `Request`, and `Depends()` resolve as normal.
- Templates are compiled once per process unless `auto_reload=True`. Keep it off in production.
- `global_init()` accepts `str` or any `os.PathLike`. Versions up to 0.1.18 accepted a `Path` but failed later with `TypeError: 'PosixPath' object is not iterable`; use `str()` there.

## Decision table

| Need | Use |
|---|---|
| Render a template from a sync or async view | `@fastapi_chameleon.template('home/index.pt')` on the view |
| Infer the template from module and function name | bare `@fastapi_chameleon.template` after `global_init()` has run |
| Redirect or return JSON from a page view | return a `fastapi.Response` subclass |
| HTML 404 instead of FastAPI's JSON | `fastapi_chameleon.not_found()` or `not_found('errors/custom.pt')` |
| Any error status with data in the template | `fastapi_chameleon.generic_error('errors/403.pt', 403, template_data={...})` |
| Non-200 status or non-HTML type from a normal view | `fastapi_chameleon.response(template_file, mimetype=..., status_code=..., **model)` |
| Non-HTML type for a decorated view | `@template('seo/sitemap.pt', mimetype='application/xml')` |
| Rendered HTML as a string | `fastapi_chameleon.engine.render(template_file, **model)` |
| Pick up template edits without restart | `global_init(folder, auto_reload=True)` |
| Re-initialise in tests | `global_init(folder, cache_init=False)` or `engine.clear()` |

## API

- `global_init(template_folder: str | os.PathLike, auto_reload: bool = False, cache_init: bool = True) -> None`. Raises `FastAPIChameleonException` for an empty or non-directory path. Idempotent by default.
- `template(template_file: str | None = None, mimetype: str = 'text/html')`. Decorator, usable bare or with arguments. Returns a signature-preserving wrapper.
- `response(template_file: str, mimetype: str = 'text/html', status_code: int = 200, **template_data) -> fastapi.Response`. Manual render. Raises `FastAPIChameleonException` if not initialised.
- `not_found(four04template_file: str = 'errors/404.pt') -> NoReturn`. Raises `FastAPIChameleonNotFoundException`.
- `generic_error(template_file: str, status_code: int, template_data: dict | None = None) -> NoReturn`. Raises `FastAPIChameleonGenericException`.
- `engine.render(template_file: str, **template_data) -> str` and `engine.clear() -> None`. Not in `__all__`; import via `fastapi_chameleon.engine`.
- `exceptions.FastAPIChameleonException` (base), `FastAPIChameleonNotFoundException` (`.template_file`), `FastAPIChameleonGenericException` (`.template_file`, `.status_code`, `.template_data`).

## Reading a failure

```text
fastapi_chameleon.exceptions.FastAPIChameleonException: Invalid return type <class 'NoneType'>, we expected a dict or fastapi.Response as the return value.
    -> the view has no return statement, or returned a model; return a dict
ValueError: Template not found: home/index.pt.
    -> path is relative to the global_init() folder; check folder, subfolder, .pt vs .html, and that global_init() ran before the view module was imported
NameError: items
    -> the template uses a variable the view did not return; add it to the dict or guard with tal:condition
INFO: 127.0.0.1 - "GET /items/9" 500   (log: FastAPIChameleonNotFoundException: The URL resulted in a 404 response.)
    -> not_found() was called outside a @template-decorated view; decorate the route or raise fastapi.HTTPException
```

Fix order: make `global_init()` run once and first with an absolute path, then make the view return a dict, then fix the template path, then read the variable or expression Chameleon names.

## Resources

- Docs: <https://mkennedy.codes/docs/fastapi-chameleon/>
- Getting started: <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/getting-started.html>
- Decorating views: <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/views.html>
- Writing templates: <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/templates.html>
- Error pages: <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/error-pages.html>
- Troubleshooting: <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/troubleshooting.html>
- Testing and CI: <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/testing.html>
- API reference: <https://mkennedy.codes/docs/fastapi-chameleon/reference/>
- llms.txt: <https://mkennedy.codes/docs/fastapi-chameleon/llms.txt>, llms-full.txt: <https://mkennedy.codes/docs/fastapi-chameleon/llms-full.txt>
- Source: <https://github.com/mikeckennedy/fastapi-chameleon>
