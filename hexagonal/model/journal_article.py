from hexagonal import db

from hexagonal.model.document import Document


class JournalArticle(Document):
    __tablename__ = 'journal_articles'

    issue_id = db.Column(db.Integer, db.ForeignKey('journal_issues.id'))
    issue = db.relationship('JournalIssue', back_populates='articles')

    __mapper_args__ = {
        'polymorphic_identity': 'journal_article'
    }
