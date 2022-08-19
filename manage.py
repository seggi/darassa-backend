from locale import currency
import os
from re import DEBUG
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from api import create_app, db


app = create_app(os.getenv('FLASK_ENV') or 'production')

cli = FlaskGroup(app)
migrate = Migrate(app, db)


@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()


@cli.command("drop_db")
def drop_db():
    db.drop_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    request_status = ["sent", "accepted", "rejected", "expired"]
    budget_options = ["Icommes", "Expenses"]
    rent_payment_option = ["Month", "Week", "Day", "Year"]


if __name__ == "__main__":
    cli()
