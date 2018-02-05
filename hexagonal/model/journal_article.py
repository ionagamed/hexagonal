from hexagonal import db

from hexagonal.model.document import Document
from hexagonal.model.helpers import ids


class JournalArticle(Document):
    """
    Journal article type of document.
    """

    __tablename__ = 'journal_articles'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    """ Integer primary key. """

    issue_id = db.Column(db.Integer, db.ForeignKey('journal_issues.id'))
    """ Foreign key to issue. """

    issue = db.relationship('JournalIssue', back_populates='articles')
    """ Issue of the journal. """

    __mapper_args__ = {
        'polymorphic_identity': 'journal_article'
    }

    def __json__(self):
        """
        JSON representation for a given instance.
        :return: JSON-serializable representation of self.
        """
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'copy_ids': ids(self.copies),
            'keywords': map(lambda x: x.name, self.keywords),
            'authors': map(lambda x: x.name, self.authors),
            'issue': self.issue
        }
