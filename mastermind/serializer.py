from marshmallow import Schema, fields, ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()

num2colors = {
    0: 'RED', #0
    1: 'GREEN', #1
    2: 'BLUE', #2
    3: 'CYAN', #3
    4: 'YELLOW', #4
    5: 'MAGENTA', #5
}
colors2num = {
    'RED': 0,
    'GREEN': 1,
    'BLUE': 2,
    'CYAN': 3,
    'YELLOW': 4,
    'MAGENTA': 5,
}


class ColorsArray(fields.Field):
    def _serialize(self, value, attr, obj):
        colors = [ num2colors[int(c)] for c in value ]
        return colors

    def _deserialize(self, value, attr, data):
        nums = []
        if type(value) is not list:
            raise ValidationError(f"{type(value)} is not list")
        if len(value) != 4:
            raise ValidationError(f"Wrong length: {len(value)}")

        for c in value:
            C = c.upper()
            if C not in colors2num:
                raise ValidationError(f"Wrong color: {c}")
            nums.append(str(colors2num[C]))

        return "".join(nums)


class PegsArray(fields.Field):
    def _serialize(self, value, attr, obj):
        full_match, color_match = obj.decode_answer()
        pegs = [ 'BLACK' for i in range(full_match) ]
        pegs.extend('WHITE' for i in range(color_match))
        return pegs


class GameSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    over = fields.Bool(dump_only=True)
    rounds_chrono = fields.Nested('RoundSchema', dump_only=True, many=True,
        only=('id', 'hand', 'answer'))


# TODO not DRY
class GameSchemaShort(ma.Schema):
    id = fields.Int(dump_only=True)


class RoundSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    game = fields.Nested(GameSchema, only=('id',))
    hand = ColorsArray()
    answer = PegsArray()


game_schema = GameSchema()
games_schema = GameSchemaShort(many=True)

round_schema = RoundSchema()
rounds_schema = RoundSchema(many=True)
