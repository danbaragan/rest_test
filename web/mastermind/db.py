from datetime import datetime
import click
from flask.cli import with_appcontext
from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
)
from playhouse.flask_utils import FlaskDB
# from .gameengine import MAX_COLORS

db_wrapper = FlaskDB()


class BaseModel(db_wrapper.Model):
    created = DateTimeField()
    modified = DateTimeField()

    def save(self, *args, **kwargs):
        self.modified = datetime.utcnow()
        super(BaseModel, self).save(*args, **kwargs)

    @classmethod
    def encode(cls, engine_ints):
        """Transform integer lists from engine to string stored in the db
        use to 'encode' game, hand, answer"""
        return "".join(str(x) for x in engine_ints)


class Game(BaseModel):
    # num_colors = IntegerField(default=MAX_COLORS)
    num_rounds = IntegerField(default=12)
    play_colors = CharField() # an array would be nice here... postgres only...
    over = BooleanField(default=False)

    @property
    def round_number(self):
        """The round number we are currently playing, zero based"""
        return self.rounds.count()

    @property
    def rounds_chrono(self):
        return self.rounds.order_by(Round.modified.desc())

    def __str__(self):
        return f"{self.id}: {self.play_colors}"

    def decode(self):
        return [ int(x) for x in self.play_colors ]

    def get_rounds(self):
        return Round.select().where(Round.game==self).order_by(Round.modified.desc())


class Round(BaseModel):
    game = ForeignKeyField(Game, backref='rounds')
    created = DateTimeField()
    hand = CharField()
    answer = CharField(null=True, default=None)

    def __str__(self):
        return f"{self.id}: {self.hand} - {self.answer}"

    # we only decode the played hand to the engine; the answer is not an input to the engine
    def decode(self):
        return [ int(x) for x in self.hand ]

    def decode_answer(self):
        match = 0
        color = 0
        if self.answer:
            match = int(self.answer[0])
            color = int(self.answer[1])

        return match, color


MODELS = [Game, Round]


def create_tables():
    with db_wrapper.database:
        db_wrapper.database.create_tables(MODELS)


def drop_tables():
    with db_wrapper.database:
        db_wrapper.database.drop_tables(MODELS)


@click.command('init-db')
@with_appcontext
def init_db_command():
    # init tables
    create_tables()
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
