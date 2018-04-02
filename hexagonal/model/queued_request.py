from hexagonal import db
from sqlalchemy import text
from sqlalchemy.ext.associationproxy import association_proxy

import datetime


class QueuedRequest(db.Model):
    __tablename__ = 'queued_requests'

    patron = db.relationship('Patron', back_populates='queued_requests')
    patron_id = db.Column(db.ForeignKey('users.id'), primary_key=True)

    document = db.relationship('Document', back_populates='queued_requests')
    document_id = db.Column(db.ForeignKey('documents.id'), index=True)

    created_at = db.Column(db.DateTime, default=text('NOW()'))
    resolved_at = db.Column(db.DateTime, default=None, nullable=True)

    priority = association_proxy('patron', 'queuing_priority')

    notified = db.Column(db.Boolean, nullable=False, default=False)

    def resolve(self):
        self.resolved_at = datetime.datetime.now()
