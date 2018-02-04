from hexagonal import db


class Publisher(db.Model):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    books = db.relationship('Book', back_populates='publisher')
    journals = db.relationship('Journal', back_populates='publisher')
