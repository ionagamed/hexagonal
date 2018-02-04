from hexagonal import db

from hexagonal.model.document import Document
from hexagonal.model.helpers import ids


class JournalArticle(Document):
    __tablename__ = 'journal_articles'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('journal_issues.id'))
    issue = db.relationship('JournalIssue', back_populates='articles')

    __mapper_args__ = {
        'polymorphic_identity': 'journal_article'
    }

    def __json__(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'copy_ids': ids(self.copies),
            'keywords': map(lambda x: x.name, self.keywords),
            'authors': map(lambda x: x.name, self.authors),
            'issue': self.issue
        }
