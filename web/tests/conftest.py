from datetime import datetime, timedelta
import os
import pytest

from mastermind import create_app


@pytest.fixture(scope='session')
def app(tmp_path_factory):
    # TODO open this in memory
    db_path = tmp_path_factory.mktemp('db') / os.getenv('DATABASE_URL', 'test.db')
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


@pytest.fixture(scope='function')
def db_games(app):
    with app.app_context():
        from mastermind.db import db_wrapper, Game

        now = datetime.utcnow()
        g1 = Game(
            created=now,
            modified=now,
            play_colors="1234",
        )
        g1.save()

        g2 = Game(
            created=now,
            modified=now,
            play_colors="5234",
            over=True
        )
        g2.save()

        db_wrapper.database.close()
        yield app, (g1,g2)

        Game.delete().execute()


@pytest.fixture
def db_rounds(db_games):
    app, games = db_games
    g1, g2 = games
    with app.app_context():
        from mastermind.db import db_wrapper, Round

        now = datetime.utcnow()
        time1 = now - timedelta(milliseconds=100)
        time2 = now
        r1 = Round(
            created=time1,
            modified=time1,
            game=g1,
            hand="0011",
            answer="21",
        )
        r1.save()
        r2 = Round(
            created=time2,
            modified=time2,
            game=g1,
            hand="2211",
        )
        r2.save()
        r3 = Round(
            created=time1,
            modified=time1,
            game=g2,
            hand="0005",
        )
        r3.save()

        db_wrapper.database.close()
        yield app, (r1, r2, r3)

        Round.delete().execute()


@pytest.fixture
def client(db_rounds):
    app, _ = db_rounds
    return app.test_client()

