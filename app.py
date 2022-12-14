import os
from re import DEBUG
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from api import create_app, db
from api.database.models import *

app = create_app(os.getenv('FLASK_ENV') or 'production')

cli = FlaskGroup(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(port=4000)
