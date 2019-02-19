from datetime import datetime, timedelta
import pytest

@pytest.fixture
def db_games(app):
    with app.app_context():
        from mastermind.db import Game

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
        )
        g2.save()


        yield app, (g1,g2)

@pytest.fixture
def db_rounds(db_games):
    app, games = db_games
    g1, g2 = games
    with app.app_context():
        from mastermind.db import Round

        now = datetime.utcnow()
        time1 = now - timedelta(milliseconds=100)
        time2 = now
        r1 = Round(
            created=time1,
            modified=time1,
            game=g1,
            hand="0011",
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

        yield app, (r1, r2, r3)


def test_game_basic(db_games):
    app, games = db_games
    g1 = games[0]
    assert not g1.over

    g1.over = True
    last_modified = g1.modified
    g1.save()

    with app.app_context():
        from mastermind.db import Game
        g1_again = Game.get(Game.id == 1)
        assert g1.modified == g1_again.modified
        assert last_modified < g1_again.modified
        assert g1_again.over


def test_game_decode(db_games):
    app, games = db_games
    g1 = games[0]
    assert g1.decode() == [1, 2, 3, 4]


def test_game_encode(db_games):
    app, games = db_games
    g1 = games[0]
    assert g1.encode([4, 3, 2, 1]) == "4321"


def test_round_encode_decode(db_rounds):
    app, rounds = db_rounds
    r1, r2, r3 = rounds
    assert r3.decode() == [0,0,0,5]
    # decode hand
    assert r3.encode([1,1,1,1]) == "1111"
    # decode answer
    assert r3.encode((2,0)) == "20"
