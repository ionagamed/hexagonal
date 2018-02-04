from hexagonal import db
from hexagonal.model.helpers import model_crud_compound

from hexagonal.model.journal_issue import journal_issue_editor


@model_crud_compound()
class Editor(db.Model):
    __tablename__ = 'editors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    journal_issues = db.relationship('JournalIssue', secondary=journal_issue_editor, back_populates='editors')
