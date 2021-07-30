import asyncio

import fastapi

import fastapi_chameleon
import fastapi_chameleon as fc


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_friendly_404_sync_method(setup_global_template):
    @fc.template('home/index.pt')
    def view_method(a, b, c):
        fastapi_chameleon.not_found()
        return {'a': a, 'b': b, 'c': c}

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 404
    assert b'<h1>This is a pretty 404 page.</h1>' in resp.body


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_friendly_404_custom_template_sync_method(setup_global_template):
    @fc.template('home/index.pt')
    def view_method(a, b, c):
        fastapi_chameleon.not_found(four04template_file='errors/other_error_page.pt')
        return {'a': a, 'b': b, 'c': c}

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 404
    assert b'<h1>Another pretty 404 page.</h1>' in resp.body


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
def test_friendly_404_async_method(setup_global_template):
    @fc.template('home/index.pt')
    async def view_method(a, b, c):
        fastapi_chameleon.not_found()
        return {'a': a, 'b': b, 'c': c}

    resp = asyncio.run(view_method(1, 2, 3))
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 404
    assert b'<h1>This is a pretty 404 page.</h1>' in resp.body
