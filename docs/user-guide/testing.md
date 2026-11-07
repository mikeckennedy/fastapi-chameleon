# Testing and CI

Here is the pleasant secret of this package: a decorated view is still just a Python function. No server, no port, no `TestClient`, no fixture that spins up an app. You call the view, you get back a `fastapi.Response`, and you look inside it. This is how the package tests itself, and it is how Shelf Life's test suite runs in well under a second.


# A fixture for the engine

The engine is module-global, one per process, so tests need two things from a fixture: initialise it before the test, and clear it afterwards so the next test starts clean.

``` python
# conftest.py
from pathlib import Path

import pytest

import fastapi_chameleon as fc


@pytest.fixture
def setup_global_template(pytestconfig):
    fc.global_init(Path(pytestconfig.rootdir, 'tests', 'templates'))
    yield
    fc.engine.clear()  # do not leak engine state between tests
```

Two details keep this reliable:

- [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) ignores repeat calls by default. If a test calls it directly with a different folder, pass `cache_init=False`.
- Always clear in teardown. A test that asserts "rendering before [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) raises" will pass or fail depending on which test ran before it otherwise, and flaky tests that depend on ordering are the kind you only notice in CI on a Friday.


# Calling views directly

``` python
# test_views.py
import asyncio

import fastapi

import fastapi_chameleon as fc


def test_index_renders(setup_global_template):
    @fc.template('home/index.pt')
    def index(name: str):
        return {'name': name}

    resp = index('Sam')
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200
    assert resp.media_type == 'text/html'
    assert 'Sam' in resp.body.decode('utf-8')


def test_async_index_renders(setup_global_template):
    @fc.template('home/index.pt')
    async def index(name: str):
        return {'name': name}

    resp = asyncio.run(index('Sam'))
    assert resp.status_code == 200


def test_missing_item_gives_404(setup_global_template):
    @fc.template('home/index.pt')
    def item(item_id: int):
        fc.not_found()

    resp = item(42)
    assert resp.status_code == 404
```

Pass view arguments positionally or by keyword, exactly as FastAPI would. Async views are one `asyncio.run()` away. If a view takes a `Request`, build one with `fastapi.Request(scope)` or use `TestClient` for that particular test.


# Through FastAPI

When the thing under test is the routing, the dependencies, or the middleware rather than the view, use FastAPI's `TestClient` against the real app. Decorated views need nothing special:

``` python
from fastapi.testclient import TestClient

from my_app.main import app


def test_home_page():
    client = TestClient(app)
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.headers['content-type'].startswith('text/html')
```

Make sure [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) runs when `my_app.main` is imported, or call it in a session fixture before the app is created.


# CI

The package has no compiled parts and two dependencies, so CI is a pytest run per interpreter and nothing more. A GitHub Actions matrix:

``` yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12', '3.13', '3.14']
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run --python ${{ matrix.python-version }} --with pytest --with-editable . pytest
```

Locally, `tox` with the `tox.ini` in the repository does the same thing across whichever interpreters you have installed.
