# Getting Started

FastAPI answers every request with JSON unless you tell it otherwise. If you are building a site that people look at in a browser, you want server-rendered HTML, and that means a template engine wired into your view functions. fastapi-chameleon does that wiring for the [Chameleon](https://chameleon.readthedocs.io/) template language with one decorator: the view returns a `dict`, the decorator renders it through a template, and FastAPI sends the HTML.

If you prefer Jinja, use the sister project [fastapi-jinja](https://github.com/AGeekInside/fastapi-jinja) instead. The two share the same design.


# Install

``` bash
uv add fastapi-chameleon
# or
pip install fastapi-chameleon
```

The package requires Python 3.10 or newer and depends only on `fastapi` and `chameleon`. You also need an ASGI server such as `uvicorn` to run the app.


# A first page

Two files are enough. The template folder is passed to [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) once, and every template path you use later is relative to it.

**`main.py`**

``` python
from pathlib import Path

import fastapi
import uvicorn

import fastapi_chameleon

app = fastapi.FastAPI()

# Point the engine at your template folder before any view is decorated.
BASE_DIR = Path(__file__).resolve().parent
fastapi_chameleon.global_init(BASE_DIR / 'templates', auto_reload=True)


@app.get('/')
@fastapi_chameleon.template('index.pt')
def hello_world():
    return {'message': "Let's go Chameleon and FastAPI!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
```

**`templates/index.pt`**

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello</title>
</head>
<body>
<h1>Hello world</h1>
<p>Your message is <strong>${message}</strong></p>
</body>
</html>
```

Run it with `python main.py` or `uvicorn main:app`, then open `http://127.0.0.1:8000`. Both ways work here because [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) runs at import time, before the decorated view is defined.


# What you get back

The decorated function now returns a `fastapi.Response`. For the request above it carries a `200` status, a `text/html` content type, and this body:

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello</title>
</head>
<body>
<h1>Hello world</h1>
<p>Your message is <strong>Let's go Chameleon and FastAPI!</strong></p>
</body>
</html>
```

Each key in the returned `dict` became a variable in the template, so `${message}` was replaced by the string the view returned. That is the whole contract: views return data, templates turn it into HTML.

Two things in the example are easy to miss and matter later:

- The route decorator `@app.get(...)` sits on the outside. `@fastapi_chameleon.template(...)` is applied directly to the function.
- `auto_reload=True` makes Chameleon re-read templates you edit, which is what you want while developing. Turn it off in production. See [Configuration](configuration.md).


# Where to go next

- [Decorating Views](views.md): the three decorator forms, what a view may return, redirects, and [response()](../reference/response.md#fastapi_chameleon.response).
- [Writing Templates](templates.md): Chameleon syntax, shared layouts, and the project layout the name inference expects.
- [Friendly Error Pages](error-pages.md): replace FastAPI's JSON 404 with your own HTML page.
- [Troubleshooting](troubleshooting.md): every error the package raises and how to fix it.
- [Testing and CI](testing.md): call views directly in pytest, no HTTP client needed.
- [Configuration](configuration.md): every [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) option, verified.
- [How It Works](how-it-works.md): module-global engine state, decoration-time decisions, exception-based error pages.
- [FAQ](faq.md).
