import asyncio

import fastapi
import pytest

import fastapi_chameleon
import fastapi_chameleon as fc


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    ("status_code", "template_file", "expected_h1_in_body"),
    [
        (fastapi.status.HTTP_400_BAD_REQUEST, "errors/404.pt", b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_401_UNAUTHORIZED, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
        (fastapi.status.HTTP_403_FORBIDDEN, "errors/404.pt", b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_404_NOT_FOUND, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
        (fastapi.status.HTTP_405_METHOD_NOT_ALLOWED, "errors/404.pt", b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_406_NOT_ACCEPTABLE, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
        (fastapi.status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED, "errors/404.pt",
         b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_408_REQUEST_TIMEOUT, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
    ],
)
def test_friendly_403_sync_method(setup_global_template, status_code, template_file, expected_h1_in_body):
    @fc.template('home/index.pt')
    def view_method(a, b, c):
        fastapi_chameleon.generic_error(template_file, status_code)
        return {'a': a, 'b': b, 'c': c}

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == status_code
    assert expected_h1_in_body in resp.body


# setup_global_template - needed as pytest mix-in.
# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    ("status_code", "template_file", "expected_h1_in_body"),
    [
        (fastapi.status.HTTP_400_BAD_REQUEST, "errors/404.pt", b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_401_UNAUTHORIZED, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
        (fastapi.status.HTTP_403_FORBIDDEN, "errors/404.pt", b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_404_NOT_FOUND, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
        (fastapi.status.HTTP_405_METHOD_NOT_ALLOWED, "errors/404.pt", b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_406_NOT_ACCEPTABLE, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
        (fastapi.status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED, "errors/404.pt",
         b'<h1>This is a pretty 404 page.</h1>'),
        (fastapi.status.HTTP_408_REQUEST_TIMEOUT, "errors/other_error_page.pt", b'<h1>Another pretty 404 page.</h1>'),
    ],
)
def test_friendly_403_async_method(setup_global_template, status_code, template_file, expected_h1_in_body):
    @fc.template('home/index.pt')
    async def view_method(a, b, c):
        fastapi_chameleon.generic_error(template_file, status_code)
        return {'a': a, 'b': b, 'c': c}

    resp = asyncio.run(view_method(1, 2, 3))
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == status_code
    assert expected_h1_in_body in resp.body
