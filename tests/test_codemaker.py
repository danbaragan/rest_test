import pytest
import json

from mastermind.db import db_wrapper, Game

def test_gameslist_get(client):
    resp = client.get('/games')
    assert resp.status_code == 200
    data = resp.json
    games = data['games']
    assert len(games) == 1
    game = games[0]
    game_id = Game.get(Game.id == game['id']).id
    assert game['id'] == game_id


def test_gamelist_new(client):
    game_ids = [ o[0] for o in Game.select(Game.id).tuples() ]
    db_wrapper.database.close()

    resp = client.post('/games')
    assert resp.status_code == 201
    data = resp.json
    assert data['id'] not in game_ids


def test_gamesdetail_get(client):
    game_id = Game.select(Game.id).tuples()[0][0]
    db_wrapper.database.close()

    resp = client.get(f'/games/{game_id}')
    assert resp.status_code == 200
    data = resp.json
    game = data['game']
    assert game['id'] == game_id
    rounds = game['rounds_chrono']
    assert len(rounds) == 2
    # TODO add date modified to serializer and do a more robust check
    # slopy check for desc order
    assert rounds[0]['id'] > rounds[1]['id']


def test_gamesdetail_get_nonexistent(client):
    resp = client.get('/games/1111111')
    assert resp.status_code == 404


def test_roundslist_get(client):
    game = Game.select()[:1][0]
    expected_rounds = game.rounds_chrono
    expected_rounds_ids = [ o.id for o in expected_rounds ]
    db_wrapper.database.close()

    resp = client.get(f"/games/{game.id}/rounds")
    assert resp.status_code == 200
    data = resp.json
    rounds = data['rounds']
    assert len(rounds) == 2
    rounds_ids = [ o['id'] for o in rounds ]
    assert rounds_ids == expected_rounds_ids


def test_roundslist_get_nonexistent(client):
    resp = client.get("/games/111111/rounds")
    assert resp.status_code == 404


def test_roundslist_post_wrong_game(client):
    # fetch a finished game
    expected_game = Game.select().where(Game.over == True)[:1][0]
    db_wrapper.database.close()

    req = {'hand': None}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 400
    data = resp.json
    assert data == {'errors': {'game': [f'No such open game: {expected_game.id}']}}


def test_roundslist_post_wrong_type(client):
    expected_game = Game.select()[:1][0]
    db_wrapper.database.close()

    req = {'hand': 'RED'}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 400
    data = resp.json
    assert data == {'errors': {'hand': ["<class 'str'> is not list"]}}


def test_roundslist_post_wrong_length(client):
    expected_game = Game.select()[:1][0]
    db_wrapper.database.close()

    req = {'hand': ['RED', 'GREEN']}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 400
    data = resp.json
    assert data == {'errors': {'hand': ['Wrong length: 2']}}


def test_roundslist_post_wrong_color(client):
    expected_game = Game.select()[:1][0]
    db_wrapper.database.close()

    req = {'hand': ['RED', 'RED', 'RED', 'notAColor']}
    resp = client.post(
        f"/games/{expected_game.id}/rounds",
        data=json.dumps(req),
        content_type='application/json',
    )
    assert resp.status_code == 400
    data = resp.json
    assert data == {'errors': {'hand': ['Wrong color: notAColor']}}


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


def test_roundsdetail_get(client):
    expected_game = Game.select()[:1][0]
    expected_rounds = expected_game.rounds[:2]
    expected_round1 = expected_rounds[0]
    expected_round2 = expected_rounds[1]
    db_wrapper.database.close()

    resp = client.get(f"/games/{expected_game.id}/rounds/{expected_round1.id}")
    assert resp.status_code == 200
    data = resp.json
    round = data['round']
    assert round['id'] == expected_round1.id
    colors = round['hand']
    assert colors == ["RED", "RED", "GREEN", "GREEN"]
    pegs = round['answer']
    assert pegs == ['BLACK', 'BLACK', 'WHITE']

    resp = client.get(f"/games/{expected_game.id}/rounds/{expected_round2.id}")
    assert resp.status_code == 200
    assert resp.json['round']['id'] == expected_round2.id
    pegs = resp.json['round']['answer']
    assert pegs == []
    

def test_roundsdetail_get_nonexistent(client):
    expected_game = Game.select()[:1][0]
    db_wrapper.database.close()

    resp = client.get(f"/games/{expected_game.id}/rounds/1111111")
    assert resp.status_code == 404
