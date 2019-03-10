from datetime import datetime, timedelta
import os
import pytest
import psycopg2

from mastermind import create_app
from mastermind import db


def create_test_db(db_name, user, password):
    con = psycopg2.connect(
        dbname='postgres',
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(f"DROP DATABASE {db_name} ;")
    except psycopg2.ProgrammingError:
        pass
    try:
        cur.execute(f"DROP USER {user} ;")
    except psycopg2.ProgrammingError:
        pass

    cur.execute(f"CREATE DATABASE {db_name} ;")
    cur.execute(f"CREATE USER {user} WITH ENCRYPTED PASSWORD '{password}';")
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};")
    con.close()


def drop_test_db(db_name, user):
    con = psycopg2.connect(
        dbname='postgres',
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(f"DROP DATABASE {db_name} ;")
    cur.execute(f"DROP USER {user} ;")
    con.close()


@pytest.fixture(scope='session')
def app(tmp_path_factory):
    user = 'testing'
    password = 'testing'
    db_name = 'testing'
    create_test_db(db_name, user, password)

    app = create_app({
        'TESTING': True,
        'DATABASE': {
            'name': db_name,
            'engine': 'playhouse.pool.PostgresqlDatabase',
            'user': user,
            'password': password,
            'host': os.getenv('DATABASE_HOST'),
        },
    })
    with app.app_context():
        db.create_tables()

    yield app

    with app.app_context():
        db.drop_tables()
    drop_test_db(db_name, user)


@pytest.fixture(scope='function')
def db_games(app):
    with app.app_context():
        now = datetime.utcnow()
        g1 = db.Game(
            created=now,
            modified=now,
            play_colors="1234",
        )
        g1.save()

        g2 = db.Game(
            created=now,
            modified=now,
            play_colors="5234",
            over=True
        )
        g2.save()

        db.db_wrapper.database.close()
        yield app, (g1, g2)

        db.Game.delete().execute()


@pytest.fixture
def db_rounds(db_games):
    app, games = db_games
    g1, g2 = games
    with app.app_context():
        now = datetime.utcnow()
        time1 = now - timedelta(milliseconds=100)
        time2 = now
        r1 = db.Round(
            created=time1,
            modified=time1,
            game=g1,
            hand="0011",
            answer="21",
        )
        r1.save()
        r2 = db.Round(
            created=time2,
            modified=time2,
            game=g1,
            hand="2211",
        )
        r2.save()
        r3 = db.Round(
            created=time1,
            modified=time1,
            game=g2,
            hand="0005",
        )
        r3.save()

        db.db_wrapper.database.close()
        yield app, (g1, g2), (r1, r2, r3)

        db.Round.delete().execute()


@pytest.fixture
def client(db_rounds):
    app, games, rounds = db_rounds
    return app.test_client()

