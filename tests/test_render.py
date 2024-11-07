import asyncio

import fastapi
# noinspection PyPackageRequirements
import pytest

import fastapi_chameleon as fc


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_cannot_decorate_missing_template(setup_global_template):
    with pytest.raises(ValueError):

        @fc.template('home/missing.pt')
        def view_method():
            return {}

        view_method()


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_requires_template_for_default_name(setup_global_template):
    with pytest.raises(ValueError):

        @fc.template(None)
        def view_method():
            return {}

        view_method()


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_default_template_name_pt(setup_global_template):
    @fc.template()
    def index(a, b, c):
        return {'a': a, 'b': b, 'c': c, 'world': 'WORLD'}

    resp = index(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200
    html = resp.body.decode('utf-8')
    assert '<h1>Hello default WORLD!</h1>' in html


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_default_template_name_no_parentheses(setup_global_template):
    @fc.template
    def index(a, b, c):
        return {'a': a, 'b': b, 'c': c, 'world': 'WORLD'}

    resp = index(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200
    html = resp.body.decode('utf-8')
    assert '<h1>Hello default WORLD!</h1>' in html


def test_default_template_name_html(setup_global_template):
    @fc.template()
    def details(a, b, c):
        return {'a': a, 'b': b, 'c': c, 'world': 'WORLD'}

    resp = details(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200
    html = resp.body.decode('utf-8')
    assert '<h1>Hello default WORLD!</h1>' in html


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_can_decorate_dict_sync_method(setup_global_template):
    @fc.template('home/index.pt')
    def view_method(a, b, c):
        return {'a': a, 'b': b, 'c': c}

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_can_decorate_dict_async_method(setup_global_template):
    @fc.template('home/index.pt')
    async def view_method(a, b, c):
        return {'a': a, 'b': b, 'c': c}

    resp = asyncio.run(view_method(1, 2, 3))
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_direct_response_pass_through():
    @fc.template('home/index.pt')
    def view_method(a, b, c):
        return fastapi.Response(content='abc', status_code=418)

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 418
    assert resp.body == b'abc'
