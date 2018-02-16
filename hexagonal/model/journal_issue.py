from hexagonal import db
from hexagonal.model.helpers import ids

journal_issue_editor = db.Table(
    'journal_issue_editor',
    db.Model.metadata,
    db.Column('journal_issue_id', db.Integer, db.ForeignKey('journal_issues.id')),
    db.Column('editor_id', db.Integer, db.ForeignKey('editors.id'))
)


class JournalIssue(db.Model):
    """
    Journal issue model.
    Internal model, gets squashed in the api.
    """

    __tablename__ = 'journal_issues'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. """

    publication_date = db.Column(db.Date, nullable=False)
    """ Publication date of this issue. """

    editors = db.relationship('Editor', secondary=journal_issue_editor, back_populates='journal_issues')
    """ Editors of this issue. """

    journal_id = db.Column(db.Integer, db.ForeignKey('journals.id'))
    """ Foreign key to journal. """

    journal = db.relationship('Journal', back_populates='issues')
    """ Journal, which contains the issue. """

    articles = db.relationship('JournalArticle', back_populates='issue')
    """ Articles of this issue. """

    def __json__(self):
        """
        JSON representation for a given instance.
        :return: JSON-serializable representation of self.
        """
        return {
            'title': self.title,
            'price': self.price,
            'copy_ids': ids(self.copies),
            'keywords': map(lambda x: x.name, self.keywords),
            'authors': map(lambda x: x.name, self.authors),
            'publication_date': self.publication_date,
            'editors': map(lambda x: x.name, self.editors),
            'journal': self.journal,
            'type': 'issue'
        }
