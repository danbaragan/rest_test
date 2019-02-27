Mastermind the flask rest
=========================

# General

A small spin of a rest backend playing [mastermind] (https://en.wikipedia.org/wiki/Mastermind_(board_game)) game.

Using flask, flask-restful, marshmallow, peewee, pytest, docker, docker-compose

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
Partial. In progress. The repo is centered on development.
Remove/rename docker-compose.override.yml for a production environment.

It has unit and integration tests: `pytest -vv`
If you have `docker-compose up` running you can do a `docker-compose exec web pytest -vv` to run the tests.
The layout is in place so one can plug different db engines, plug through different wsgi, etc
But I wouldn't call this production ready at all.
Notably, egg/wheel/installation code is missing.

### time taken should be 6-8h
  No way. It took at least 2x8h. (and the docker part is still in progress)


# Install & Run
 - Have docker and docker-compose
 - docker-compose up
 - http://127.0.0.1/hello
 - docker-compose exec web pytest -vv # to run the tests

