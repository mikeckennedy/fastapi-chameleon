import asyncio

import fastapi
import pytest

import fastapi_chameleon
import fastapi_chameleon as fc

@pytest.mark.parametrize(
    ("status_code", "template_file", "template_data", "expected_p_in_body"),
    [
        (fastapi.status.HTTP_400_BAD_REQUEST, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_401_UNAUTHORIZED, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_402_PAYMENT_REQUIRED, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_403_FORBIDDEN, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_404_NOT_FOUND, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
    ]
)
def test_data_friendly_generic_sync(setup_global_template, status_code,
                                    template_file, template_data, expected_p_in_body):
    @fc.template('home/index.pt')
    def view_method(a, b, c):
        fastapi_chameleon.generic_error(template_file, status_code, template_data=template_data)
        return {'a': a, 'b': b, 'c': c}

    resp = view_method(1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == status_code
    assert expected_p_in_body in resp.body


@pytest.mark.parametrize(
    ("status_code", "template_file", "template_data", "expected_p_in_body"),
    [
        (fastapi.status.HTTP_400_BAD_REQUEST, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_401_UNAUTHORIZED, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_402_PAYMENT_REQUIRED, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_403_FORBIDDEN, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
        (fastapi.status.HTTP_404_NOT_FOUND, "errors/error_with_data.pt",
         {"test_data": "this error is given with data"}, b"<p>this error is given with data</p>"),
    ]
)
def test_data_friendly_generic_async(setup_global_template, status_code,
                                    template_file, template_data, expected_p_in_body):
    @fc.template('home/index.pt')
    async def view_method(a, b, c):
        fastapi_chameleon.generic_error(template_file, status_code, template_data=template_data)
        return {'a': a, 'b': b, 'c': c}

    resp = asyncio.run(view_method(1, 2, 3))
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == status_code
    assert expected_p_in_body in resp.body

