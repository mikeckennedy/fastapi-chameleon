import pytest

import fastapi_chameleon as fc
from fastapi_chameleon.exceptions import FastAPIChameleonException


def test_cannot_decorate_with_missing_init():
    fc.engine.clear()

    with pytest.raises(FastAPIChameleonException):

        @fc.template('home/index.pt')
        def view_method(a, b, c):
            return {'a': a, 'b': b, 'c': c}

        view_method(1, 2, 3)


def test_can_call_init_with_good_path(test_templates_path):
    fc.global_init(str(test_templates_path), cache_init=False)

    # Clear paths so as to no affect future tests
    fc.engine.clear()


def test_can_call_init_with_pathlib_path(test_templates_path):
    # A pathlib.Path used to pass validation but break inside Chameleon's loader at render time.
    fc.global_init(test_templates_path, cache_init=False)
    try:
        assert fc.engine.template_path == str(test_templates_path)
        html = fc.engine.render('home/index.pt', a=1, b=2, c=3)
        assert '<h1>' in html
    finally:
        fc.engine.clear()


def test_cannot_call_init_with_bad_path(test_templates_path):
    bad_path = test_templates_path / 'missing'
    with pytest.raises(Exception):
        fc.global_init(str(bad_path), cache_init=False)
