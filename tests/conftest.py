from pathlib import Path

import pytest

import fastapi_chameleon as fc


@pytest.fixture
def test_templates_path(pytestconfig):
    return Path(pytestconfig.rootdir, 'tests', 'templates')


@pytest.fixture
def setup_global_template(test_templates_path):
    fc.global_init(str(test_templates_path))
    yield
    # Clear paths so as to no affect future tests
    fc.engine.clear()
