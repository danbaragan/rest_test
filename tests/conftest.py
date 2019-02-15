import os

import pytest

from mastermind import create_app


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / os.getenv('DATABASE', 'test.db')
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
