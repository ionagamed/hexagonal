from hexagonal import db


class Journal(db.Model):
    """
    Journal model.
    Internal model, gets squashed in the api.
    """

    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    publisher = db.relationship('Publisher', back_populates='journals')
    issues = db.relationship('JournalIssue', back_populates='journal')

    def __json__(self):
        return {
            'title': self.title,
            'publisher': self.publisher.name
        }
