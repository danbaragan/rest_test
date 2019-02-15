import os
from pathlib import Path

from flask import Flask
from dotenv import load_dotenv

def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__)
    instance_path = Path(app.instance_path)
    app.config.from_mapping(
        DATABASE=instance_path / os.getenv('DATABASE'),
        SECRET_KEY=os.getenv('SECRET_KEY'),
    )

    if test_config:
        app.config.from_mapping(test_config)

    instance_path.mkdir(parents=True, exist_ok=True)

    @app.route('/hello')
    def hello():
        return "Hello world!"

    return app
