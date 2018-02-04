from hexagonal import db

from hexagonal.model.author import document_author


document_keyword = db.Table(
    'document_keyword',
    db.Model.metadata,
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'))
)


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    copies = db.Column(db.Integer, nullable=False, default=1)

    keywords = db.relationship('Keyword', secondary=document_keyword, back_populates='documents')
    authors = db.relationship('Author', secondary=document_author, back_populates='documents')

    type = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'document'
    }
