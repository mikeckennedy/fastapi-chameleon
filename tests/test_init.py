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


def test_cannot_call_init_with_bad_path(test_templates_path):
    bad_path = test_templates_path / 'missing'
    with pytest.raises(Exception):
        fc.global_init(str(bad_path), cache_init=False)
