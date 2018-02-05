from hexagonal import db


class Journal(db.Model):
    """
    Journal model.
    Internal model, gets squashed in the api.
    """

    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. 
    """
    title = db.Column(db.String(120), nullable=False)
    """ Title of the journal. """

    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    """ Foreign key to publisher. """

    publisher = db.relationship('Publisher', back_populates='journals')
    """ Publisher of the journal. """

    issues = db.relationship('JournalIssue', back_populates='journal')
    """ Issues of the journal. """

    def __json__(self):
        """
        JSON representation for a given instance.
        :return: JSON-serializable representation of self.
        """
        return {
            'title': self.title,
            'publisher': self.publisher.name
        }
