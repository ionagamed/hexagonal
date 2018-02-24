from hexagonal import db

from hexagonal.model.document import Document


class JournalArticle(Document):
    """
    Journal article type of document.
    """

    __tablename__ = 'journal_articles'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    """ Integer primary key. """

    issue_editor = db.Column(db.String(80))
    """ Editor of the issue. """

    issue_publication_date = db.Column(db.Date)
    """ Publication date of the issue. """

    journal = db.Column(db.String(80))
    """ Journal. """

    __mapper_args__ = {
        'polymorphic_identity': 'journal_article'
    }
