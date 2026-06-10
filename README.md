# fastapi-chameleon

[![PyPI version](https://img.shields.io/pypi/v/fastapi-chameleon.svg)](https://pypi.org/project/fastapi-chameleon/)
[![Python versions](https://img.shields.io/pypi/pyversions/fastapi-chameleon.svg)](https://pypi.org/project/fastapi-chameleon/)
[![License](https://img.shields.io/pypi/l/fastapi-chameleon.svg)](https://github.com/mikeckennedy/fastapi-chameleon/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkennedy.codes-blue.svg)](https://mkennedy.codes/docs/fastapi-chameleon/)

Adds integration of the [Chameleon template language](https://chameleon.readthedocs.io/) to [FastAPI](https://fastapi.tiangolo.com/). If you are interested in Jinja instead, see the sister project: [github.com/AGeekInside/fastapi-jinja](https://github.com/AGeekInside/fastapi-jinja).

**Documentation:** full docs and a per-function API reference live at [mkennedy.codes/docs/fastapi-chameleon](https://mkennedy.codes/docs/fastapi-chameleon/). An [llms.txt](https://mkennedy.codes/docs/fastapi-chameleon/llms.txt) index is available for AI coding tools.

## Features

- **One decorator** turns a FastAPI view into a server-rendered HTML page: return a `dict`, get a rendered template.
- **Sync and async views** are both fully supported.
- **`fastapi.Response` pass-through**: return a `Response` (redirect, JSON, etc.) from a decorated view and the template is skipped entirely.
- **Friendly error pages**: `not_found()` renders a custom 404 page, `generic_error()` renders any template with any status code.
- **Template name inference**: leave the template name off and it's derived from the module and function name.
- **Dev mode**: `auto_reload=True` picks up template edits without restarting the server.
- **Fully typed**: ships inline type hints with a `py.typed` marker (PEP 561). The decorator uses `ParamSpec`-based overloads and `functools.wraps`, so a decorated view keeps its exact parameter signature — FastAPI's dependency injection and type checkers like [ty](https://github.com/astral-sh/ty) and [pyrefly](https://pyrefly.org/) keep working.
- **Tiny dependency footprint**: just `fastapi` and `chameleon`.

## Installation

```bash
pip install fastapi-chameleon
```

## Quick start

A minimal but complete app — two files.

**`main.py`**

```python
from pathlib import Path

import fastapi
import uvicorn

import fastapi_chameleon

app = fastapi.FastAPI()

# Point the engine at your template folder (do this before views are registered).
BASE_DIR = Path(__file__).resolve().parent
fastapi_chameleon.global_init(str(BASE_DIR / 'templates'), auto_reload=True)


@app.get('/')
@fastapi_chameleon.template('index.pt')
def hello_world():
    return {'message': "Let's go Chameleon and FastAPI!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
```

**`templates/index.pt`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>Hello world</h1>
<p>Your message is <strong>${message}</strong></p>
</body>
</html>
```

Run it with `python main.py` (or `uvicorn main:app`) and visit `http://127.0.0.1:8000`. The dict returned from the view becomes the template's variables: `{'message': ...}` renders into `${message}`.

Chameleon templates are plain HTML5 with `${expr}` interpolation plus the full TAL attribute language (`tal:repeat`, `tal:content`, and friends) in either `.pt` or `.html` files.

Note the decorator order: the route decorator (`@app.get(...)`) goes on the outside, and `@fastapi_chameleon.template(...)` is applied directly to the view function.

## Usage

### Project layout

Create a folder within your web app to hold the templates, such as:

```
├── main.py
├── views.py
│
└── templates
    ├── home
    │   └── index.pt
    ├── errors
    │   └── 404.pt
    └── shared
        └── layout.pt
```

In the app startup, tell the library about the folder you wish to use:

```python
from pathlib import Path
import fastapi_chameleon

dev_mode = True

BASE_DIR = Path(__file__).resolve().parent
template_folder = str(BASE_DIR / 'templates')
fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)
```

`global_init()` validates the folder (it raises `FastAPIChameleonException` if the path is empty or not an existing directory) and is idempotent by default: a second call is a no-op while templates are already initialized. Pass `cache_init=False` to force re-initialization (handy in tests).

> **Order matters:** call `global_init()` *before* importing/registering your view modules. Template name inference (below) resolves at decoration time; if the engine isn't initialized yet, the path silently defaults to `templates/` relative to the current working directory, which may not be what you want. If you always pass explicit template names, this is much less of a concern.

### Decorating views

Then just decorate the FastAPI view methods (works on sync and async methods):

```python
@router.post('/')
@fastapi_chameleon.template('home/index.pt')
async def home_post(request: Request):
    form = await request.form()
    vm = PersonViewModel(**form)

    return vm.dict()  # {'first': 'Michael', 'last': 'Kennedy', ...}
```

The view method should return a `dict` to be passed as variables/values to the template.

If a `fastapi.Response` is returned, the template is skipped and the response along with `status_code` and other values is directly passed through. This is common for redirects and error responses not meant for this page template:

```python
@router.post('/account/login')
@fastapi_chameleon.template('account/login.pt')
async def login(request: Request):
    user = await try_login(request)
    if user:
        return fastapi.responses.RedirectResponse('/account', status_code=302)

    return {'error': 'Invalid login'}  # re-render the form with an error
```

Returning anything other than a `dict` or a `fastapi.Response` raises `FastAPIChameleonException`.

The decorator also accepts a `mimetype` for non-HTML output, e.g. `@fastapi_chameleon.template('seo/sitemap.pt', mimetype='application/xml')`.

### Three ways to use the decorator

```python
@fastapi_chameleon.template('home/index.pt')   # explicit template file
@fastapi_chameleon.template()                  # inferred template name
@fastapi_chameleon.template                    # bare form, also inferred
```

When no template name is given, it's derived from where the view lives:

- The file is `{module}/{function_name}` under the template folder, where `module` is the last segment of the view's dotted module name.
- An `.html` file is preferred; if it doesn't exist, `.pt` is the fallback.
- Example: `def index()` in `views/home.py` resolves to `templates/home/index.html`, falling back to `templates/home/index.pt`.

This resolution happens once at import time, so there is zero per-request filesystem overhead.

A few error behaviors worth knowing:

- Calling a decorated view without ever calling `global_init()` raises `FastAPIChameleonException` at request time.
- Referencing a template file that doesn't exist raises `ValueError` (from Chameleon's loader) when the view is called.

## Friendly 404s and errors

A common technique for user-friendly sites is to use a [custom HTML page for 404 responses](https://www.instantshift.com/2019/10/16/user-friendly-404-pages/). This is especially important in FastAPI because FastAPI returns a 404 response + JSON by default. This library has support for friendly 404 pages using the `fastapi_chameleon.not_found()` function.

Here's an example:

```python
@router.get('/catalog/item/{item_id}')
@fastapi_chameleon.template('catalog/item.pt')
async def item(item_id: int):
    item = service.get_item_by_id(item_id)
    if not item:
        fastapi_chameleon.not_found()

    return item.dict()
```

This will render a 404 response using the template file `templates/errors/404.pt`. You can specify another template to use for the response, but it's not required:

```python
fastapi_chameleon.not_found(four04template_file='errors/custom_404.pt')
```

`not_found()` works by raising an exception, so execution stops right there — code after the call never affects the response. The 404 template is rendered with an empty model.

Because the decorator is what catches the exception, you can call `not_found()` or `generic_error()` anywhere beneath a decorated view — deep in a service or data-access layer works fine. The flip side: calling them from a route that is *not* decorated with `@fastapi_chameleon.template` (or from middleware/dependencies) leaves the exception unhandled and FastAPI will return a 500 instead of your error page.

If you need to return errors other than `Not Found` (status code `404`), you can use a more generic function: `fastapi_chameleon.generic_error()`. It lets you render any error template with any status code:

```python
@router.get('/catalog/item/{item_id}')
@fastapi_chameleon.template('catalog/item.pt')
async def item(item_id: int):
    item = service.get_item_by_id(item_id)
    if not item:
        fastapi_chameleon.generic_error('errors/unauthorized.pt',
                                        fastapi.status.HTTP_401_UNAUTHORIZED)

    return item.dict()
```

You can also pass data into the error template via the optional `template_data` dict:

```python
fastapi_chameleon.generic_error('errors/500.pt', 500,
                                template_data={'detail': 'Something went sideways.'})
```

Note that error pages are always rendered as `text/html`, regardless of the `mimetype` passed to the `@template` decorator.

## Manual rendering with `response()`

If you need full manual control — say, a non-200 status code or a non-HTML mimetype — without going through the decorator, use `response()`:

```python
import fastapi_chameleon

@router.get('/report')
def report():
    return fastapi_chameleon.response('reports/summary.pt',
                                      status_code=202,
                                      title='Monthly summary')
```

It renders the template with the keyword arguments as the model and wraps the result in a `fastapi.Response` with your chosen `mimetype` (default `'text/html'`) and `status_code` (default `200`).

## API reference

Full, per-function docs are at [mkennedy.codes/docs/fastapi-chameleon](https://mkennedy.codes/docs/fastapi-chameleon/). The summary below mirrors the public surface.

Everything public is importable straight from `fastapi_chameleon`:

```python
__all__ = ['template', 'global_init', 'not_found', 'response', 'generic_error']
```

| Function | Signature | Purpose |
|---|---|---|
| `global_init` | `global_init(template_folder: str, auto_reload: bool = False, cache_init: bool = True) -> None` | Initialize the template engine once at startup. No-op if already initialized (unless `cache_init=False`). |
| `template` | `template(template_file=None, mimetype='text/html')` | Decorator for view functions. Usable bare, with empty parens, or with an explicit template path. |
| `response` | `response(template_file: str, mimetype: str = 'text/html', status_code: int = 200, **template_data) -> fastapi.Response` | Render a template and wrap it in a `Response` with full manual control. |
| `not_found` | `not_found(four04template_file: str = 'errors/404.pt') -> NoReturn` | Abort the view and render a friendly 404 page (always raises). |
| `generic_error` | `generic_error(template_file: str, status_code: int, template_data: Optional[dict] = None) -> NoReturn` | Abort the view and render any error template with any status code (always raises). |

Two more functions live in `fastapi_chameleon.engine` (not exported at package level):

| Function | Signature | Purpose |
|---|---|---|
| `engine.render` | `render(template_file: str, **template_data) -> str` | Render a template directly to an HTML string. |
| `engine.clear` | `clear() -> None` | Reset the cached loader and template path — the test-isolation hook. |

Exceptions, in `fastapi_chameleon.exceptions`:

- `FastAPIChameleonException(Exception)` — base class; also raised for bad `global_init` input, missing init at render time, and invalid view return types.
- `FastAPIChameleonNotFoundException` — raised by `not_found()`; carries `.template_file` and `.message`.
- `FastAPIChameleonGenericException` — raised by `generic_error()`; carries `.template_file`, `.status_code`, `.message`, and `.template_data`.

## Dev mode, caching, and performance

- `auto_reload` defaults to `False`: Chameleon caches compiled templates for production performance. Set `auto_reload=True` during development to pick up template edits without restarting.
- Engine state is a single module-global template loader per process. Call `global_init()` once before serving requests; after that the loader is read-only.

## Testing your views

Decorated views remain plain callables — no `TestClient` required. Call them directly (or via `asyncio.run()` for async views) and inspect the returned `fastapi.Response`:

```python
# conftest.py
from pathlib import Path

import pytest
import fastapi_chameleon as fc

@pytest.fixture
def test_templates_path(pytestconfig):
    return Path(pytestconfig.rootdir, 'tests', 'templates')

@pytest.fixture
def setup_global_template(test_templates_path):
    fc.global_init(str(test_templates_path))
    yield
    fc.engine.clear()  # don't leak engine state between tests
```

```python
# test_views.py
# index_view is any view function decorated with @fastapi_chameleon.template(...)
def test_index_renders(setup_global_template):
    resp = index_view()
    assert resp.status_code == 200
    assert 'Hello' in resp.body.decode('utf-8')
```

This is exactly the pattern this project's own [test suite](https://github.com/mikeckennedy/fastapi-chameleon/tree/main/tests) uses.

## Example app

A small, runnable FastAPI app showing sync and async views lives in the [`example/`](https://github.com/mikeckennedy/fastapi-chameleon/tree/main/example) folder:

```bash
cd example
python example_app.py
```

Then visit `http://127.0.0.1:8000` (and `/async` for the async view). Note that the example calls `global_init()` at runtime (from `main()`, via an `add_chameleon()` helper) rather than at import time, so run it with `python example_app.py` rather than via the `uvicorn` CLI.

## Requirements

- Python **3.10+** (supports up through 3.14)
- `fastapi`
- `chameleon`

That's the entire runtime dependency list.

## Contributing

PRs and issues are welcome at [github.com/mikeckennedy/fastapi-chameleon](https://github.com/mikeckennedy/fastapi-chameleon).

```bash
git clone https://github.com/mikeckennedy/fastapi-chameleon.git
cd fastapi-chameleon
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"   # pytest + ty + pyrefly
pytest
```

Code style is enforced with [Ruff](https://docs.astral.sh/ruff/) (`ruff.toml`: 120-character lines, single quotes), and the package is type-checked with [ty](https://github.com/astral-sh/ty) and [pyrefly](https://pyrefly.org/). Please run the full check before submitting:

```bash
ruff check .
ty check fastapi_chameleon
pyrefly check fastapi_chameleon
pytest
```

(The `requirements-dev.txt` file additionally pulls in the docs toolchain — `great-docs`, `uvicorn`, `twine` — for building the documentation site.)

## License

MIT — see [LICENSE](https://github.com/mikeckennedy/fastapi-chameleon/blob/main/LICENSE).

Created by [Michael Kennedy](https://github.com/mikeckennedy) of [Talk Python](https://talkpython.fm).
