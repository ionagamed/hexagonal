from hexagonal import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(128))


