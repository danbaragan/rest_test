Mastermind the flask rest
=========================

# General

A small spin of a rest backend playing [mastermind] (https://en.wikipedia.org/wiki/Mastermind_(board_game)) game.

Using flask, flask-restful, marshmallow, peewee, pytest, dotenv

# Requirements

There were several requirements for this that were met in various degrees

### create a game; give feedback for code guess, check game history
  - create a new game: POST no data at endpoint /games
  - list games: GET /games
  - game details GET /games/<id>
  - list game rounds: GET /games/<id>/rounds
  - list game rounds details: GET /game/<id>/rounds/<id>
  - play a round POST {'hand': ['color', 'color', 'color', 'color']} at /games/<id>/rounds
    you will get and answer object similar to {'answer': ['BLACK', 'BLACK', 'WHITE']}
    it is your task to decide that you won the game (4 blacks).
    You cannot play a next round in a finished game. The game ends after 12 rounds.

### the code should be production ready
Partial.
There is .env detection that can be used to steer the app towards prod, dev, staging
test is separate, by `create_app` factory argument.
It has unit and integration tests: `pytest -vv`
The layout is in place so one can plug different db engines, plug through different wsgi, etc
But I wouldn't call this production ready at all.
Notably, egg/installation code is missing.

### time taken should be 6-8h
  No way. It took at least 2x8h.


# Install & Run
 - Have a linux/macos system
 - Have python3 (>3.6, I use f strings)
 - Have virtualenv
 - virtualenv -p python3 virtualenvMasterind
 - pip install -r requirements.txt
 - cp env.sample .env # and choose values (the defaults should be fine)
 - pytest -vv
 - flask run

