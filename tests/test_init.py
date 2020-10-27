import os

import pytest

import fastapi_jinja as fj

here = os.path.dirname(__file__)
folder = os.path.join(here, "templates")


def test_can_call_init_with_good_path():
    fj.global_init(folder, cache_init=False)
    # assert True, "dummy sample test"


def test_cannot_call_init_with_bad_path():
    with pytest.raises(Exception):
        fj.global_init(folder + "missing", cache_init=False)
