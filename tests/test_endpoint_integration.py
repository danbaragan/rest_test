import pytest
import json
from mastermind.db import db_wrapper, Game, Round

def test_roundslist_post(client):
    expected_game = Game.select()[:1][0]
    db_wrapper.database.close()

    req = {'hand': ['GREEN', 'BLUE', 'YELLOW', 'MAGENTA']}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 201
    data = resp.json
    assert data == {'answer': ['BLACK', 'BLACK', 'WHITE']}


def test_roundslist_post_win(client):
    expected_game = Game.select()[:1][0]
    db_wrapper.database.close()

    # should be case insensitive
    req = {'hand': ['GREEN', 'BLUE', 'cyan', 'yellow']}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 201
    data = resp.json
    # win condition
    assert data == {'answer': ['BLACK', 'BLACK', 'BLACK', 'BLACK']}


def test_roundslist_post_win_edge(client):
    expected_game = Game.select()[:1][0]
    # we have 2 rounds from conftest, make it so that the game ends on next round
    expected_game.num_rounds = 3
    expected_game.save()
    db_wrapper.database.close()

    # should be case insensitive
    # win combination
    req = {'hand': ['GREEN', 'BLUE', 'cyan', 'yellow']}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 201
    data = resp.json
    # win condition
    assert data == {'answer': ['BLACK', 'BLACK', 'BLACK', 'BLACK']}

    game = Game.get(Game.id == expected_game.id)
    assert game.over


def test_roundslist_post_loose(client):
    expected_game = Game.select()[:1][0]
    # we have 2 rounds from conftest, make it so that the game ends on next round
    expected_game.num_rounds = 3
    expected_game.save()
    db_wrapper.database.close()

    # should be case insensitive
    # NOT win combination
    req = {'hand': ['red', 'BLUE', 'cyan', 'yellow']}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 201
    data = resp.json
    # win condition
    assert data == {'answer': ['BLACK', 'BLACK', 'BLACK']}

    game = Game.get(Game.id == expected_game.id)
    # game is over, but player did not win
    assert game.over

