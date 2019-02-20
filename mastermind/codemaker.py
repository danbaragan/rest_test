from datetime import datetime

from flask import request
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask_restful import Resource

from .db import Game, Round
from .gameengine import random_game, compute_answer
from .serializer import game_schema, games_schema, round_schema, rounds_schema


class GamesList(Resource):
    def get(self):
        open_games_q = Game.select().where(Game.over == False)
        open_games = games_schema.dump(open_games_q).data
        return {
            'games': open_games,
        }

    def post(self):
        now = datetime.utcnow()
        game = random_game()
        g = Game(
            created=now,
            modified=now,
            play_colors=Game.encode(game),
        )
        g.save()
        
        return {'id': g.id}, 201


class GamesDetail(Resource):
    def get(self, game_id):
        try:
            g = Game.get(Game.id == game_id)
        except:
            return {}, 404

        game = game_schema.dump(g).data
        return {
            'game': game,
        }


class RoundsList(Resource):
    def get(self, game_id):
        try:
            game_rounds_q = Game.get(Game.id == game_id).rounds_chrono
        except:
            return {}, 404

        game_rounds = rounds_schema.dump(game_rounds_q).data

        return {
            'rounds': game_rounds,
        }

    def post(self, game_id):
        try:
            game = Game.get(Game.id == game_id, Game.over == False)
        except:
            return {'errors': {'game': [f'No such open game: {game_id}']}}, 400

        round_json_data = request.get_json()
        round_data, errors = round_schema.load(round_json_data)
        if errors:
            return {'errors': errors}, 400

        now = datetime.utcnow()

        # FIXME created and modified will not be the same initially
        # FIXME this all part is fragile, should be with database.atomic
        r = Round(
            created=now,
            game=game,
            **round_data,
        )
        answer_ints = compute_answer(game.decode(), r.decode())
        r.answer = Round.encode(answer_ints)
        # check game win
        # check game over
        # FIXME all this looks like game logic. It is weird to be here. No more time - it is what it is
        if answer_ints[0] == 4 or game.round_number + 1 == game.num_rounds:
            game.over = True

        r.save()
        game.save()

        computed_round = round_schema.dump(r).data
        return {'answer': computed_round['answer']}, 201


class RoundsDetail(Resource):
    def get(self, game_id, round_id):
        try:
            round_q = Round.select().where(Round.game == game_id, Round.id == round_id)[0]
        except:
            return {}, 404

        game_round = round_schema.dump(round_q).data
        return {
            'round': game_round,
        }
