from hexagonal.auth import register_account
from hexagonal.model.user import User
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.loan import Loan
from hexagonal import db

ionagamed = User.query.filter(User.login == 'ionagamed').first()
if ionagamed is None:
    ionagamed = register_account(
        login='ionagamed',
        password='123',
        role='student-patron',

        address='123',
        phone='123',
        card_number=123,
        name='Leonid Lygin'
    )
db.session.add(ionagamed)

books = []
for i in range(1, 4):
    b = Book.query.filter(Book.title == 'Avatar, Chapter {}'.format(i)).first()
    if b is None:
        b = Book(
            title='Avatar, Chapter {}'.format(i),
            edition=1
        )
    db.session.add(b)

    if DocumentCopy.query.filter(DocumentCopy.document_id == b.id).count() < 2:
        cp1 = DocumentCopy(document=b)
        db.session.add(cp1)
        cp2 = DocumentCopy(document=b)
        db.session.add(cp2)
    books.append(b)

db.session.commit()
