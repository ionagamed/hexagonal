from hexagonal import db
from hexagonal.model.helpers import model_crud_compound

journal_issue_editor = db.Table(
    'journal_issue_editor',
    db.Model.metadata,
    db.Column('journal_issue_id', db.Integer, db.ForeignKey('journal_issues.id')),
    db.Column('editor_id', db.Integer, db.ForeignKey('editors.id'))
)


@model_crud_compound()
class JournalIssue(db.Model):
    __tablename__ = 'journal_issues'

    id = db.Column(db.Integer, primary_key=True)
    publication_date = db.Column(db.Date, nullable=False)
    editors = db.relationship('Editor', secondary=journal_issue_editor, back_populates='journal_issues')
    journal_id = db.Column(db.Integer, db.ForeignKey('journals.id'))
    journal = db.relationship('Journal', back_populates='issues')
    articles = db.relationship('JournalArticle', back_populates='issue')
