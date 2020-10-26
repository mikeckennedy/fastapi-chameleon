import os

import pytest

import fastapi_chameleon as fc

here = os.path.dirname(__file__)
folder = os.path.join(here, 'templates')


def test_can_call_init_with_good_path():
    fc.global_init(folder, cache_init=False)
    # assert True, "dummy sample test"


def test_cannot_call_init_with_bad_path():
    with pytest.raises(Exception):
        fc.global_init(folder + 'missing', cache_init=False)
