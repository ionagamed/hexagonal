from hexagonal import db


class Author():
    name = db.Column(db.String(80), unique=True, index=True)