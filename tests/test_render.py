import asyncio
import os

import fastapi
# noinspection PyPackageRequirements
import pytest

import fastapi_jinja as fj

here = os.path.dirname(__file__)
folder = os.path.join(here, 'templates')


def test_cannot_decorate_missing_template():
    with pytest.raises(ValueError):
        @fj.template('home/missing.j2')
        def view_method():
            return {}

        view_method()


def test_can_decorate_dict_sync_method():
    @fj.template('home/index.j2')
    def view_method(a, b, c):
        return {'a': a, 'b': b, 'c': c}

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_can_decorate_dict_async_method():
    @fj.template('home/index.j2')
    async def view_method(a, b, c):
        return {'a': a, 'b': b, 'c': c}

    resp = asyncio.run(view_method(1, 2, 3))
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_direct_response_pass_through():
    @fj.template('home/index.j2')
    def view_method(a, b, c):
        return fastapi.Response(content='abc', status_code=418)

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 418
    assert resp.body == b"abc"
