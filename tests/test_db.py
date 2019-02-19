import pytest


def test_game_basic(db_games):
    app, games = db_games
    g1 = games[0]
    assert not g1.over

    g1.over = True
    last_modified = g1.modified
    g1.save()

    with app.app_context():
        from mastermind.db import Game
        g1_again = Game.get(Game.id == g1.id)
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
