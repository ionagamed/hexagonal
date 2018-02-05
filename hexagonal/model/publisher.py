from hexagonal import db


class Publisher(db.Model):
    """
    Publisher model.
    Internal model, gets squashed in the api.
    """

    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. """

    name = db.Column(db.String(120))
    """ Name of the publisher. """

    books = db.relationship('Book', back_populates='publisher')
    """ Books published by this publisher. """

    journals = db.relationship('Journal', back_populates='publisher')
    """ Journals published by this publisher. """
