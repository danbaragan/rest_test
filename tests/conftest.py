import os

import pytest

from mastermind import create_app


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / os.getenv('DATABASE_URL', 'test.db')
    app = create_app({
        'TESTING': True,
        'DATABASE': {
            'name': db_path,
            'engine': 'playhouse.pool.SqliteDatabase',
        },
    })

    with app.app_context():
        from mastermind.db import create_tables
        create_tables()

    yield app

    with app.app_context():
        from mastermind.db import drop_tables
        drop_tables



@pytest.fixture
def client(app):
    return app.test_client()
