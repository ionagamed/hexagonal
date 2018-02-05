from hexagonal import db

from hexagonal.model.journal_issue import journal_issue_editor


class Editor(db.Model):
    """
    Editor for a journal.
    Internal class, gets squashed in the api.
    """

    __tablename__ = 'editors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    journal_issues = db.relationship('JournalIssue', secondary=journal_issue_editor, back_populates='editors')
