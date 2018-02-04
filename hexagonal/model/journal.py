from hexagonal import db
from hexagonal.model.helpers import model_crud_compound


@model_crud_compound()
class Journal(db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    publisher = db.relationship('Publisher', back_populates='journals')
    issues = db.relationship('JournalIssue', back_populates='journal')
