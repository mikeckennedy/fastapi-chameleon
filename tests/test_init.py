import os

import pytest

import fastapi_chameleon as fc
from fastapi_chameleon.exceptions import FastAPIChameleonException

here = os.path.dirname(__file__)
folder = os.path.join(here, 'templates')


def test_cannot_decorate_with_missing_init():
    fc.engine.template_path = None

    with pytest.raises(FastAPIChameleonException):
        @fc.template('home/index.pt')
        def view_method(a, b, c):
            return {"a": a, "b": b, "c": c}

        view_method(1, 2, 3)


def test_can_call_init_with_good_path():
    fc.global_init(folder, cache_init=False)


def test_cannot_call_init_with_bad_path():
    with pytest.raises(Exception):
        fc.global_init(folder + 'missing', cache_init=False)
