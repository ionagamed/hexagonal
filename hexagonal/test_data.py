import datetime

from hexagonal.auth import register_account
from hexagonal.model.user import User
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.loan import Loan
from hexagonal.model.librarian import Librarian
from hexagonal import db, AVMaterial, JournalArticle, StudentPatron

ionagamed = User.query.filter(User.login == 'ionagamed').first()
if ionagamed is None:
    # ionagamed = Librarian('ionagamed','123','Leonid Lyigin','Innopolis','123')
    ionagamed = register_account(
        login='ionagamed',
        password='123',
        role=StudentPatron,

        address='123',
        phone='123',
        card_number=123,
        name='Leonid Lygin'
    )
db.session.add(ionagamed)
db.session.commit()
# ionagamed = StudentPatron.query.filter(StudentPatron.login == 'ionagamed').first()

books = []
for i in range(1, 10):
    b = Book.query.filter(Book.title == 'Avatar, Chapter {}'.format(i)).first()
    if b is None:
        b = Book(
            title='Avatar, Chapter {}'.format(i),
            price=100,
            keywords=['manga', 'action'],
            authors=['Japanese folklore'],
            edition=1,
            bestseller=False,
            publisher='Japanese Publisher',
            reference=False,
            publishment_year=1980
        )
    db.session.add(b)

    if DocumentCopy.query.filter(DocumentCopy.document_id == b.id).count() < 1:
        cp1 = DocumentCopy(document=b)
        db.session.add(cp1)
        cp2 = DocumentCopy(document=b)
        db.session.add(cp2)
    books.append(b)

avs = []

av1 = AVMaterial.query.filter(AVMaterial.title == 'The Fat of the Land').first()
if av1 is None:
    av1 = AVMaterial(
        title='The Fat of the Land',
        price=150,
        keywords=['rave', 'music'],
        authors=['The Prodigy']
    )
    db.session.add(av1)
if DocumentCopy.query.filter(DocumentCopy.document_id == av1.id).count() < 2:
    cp1 = DocumentCopy(document=av1)
    db.session.add(cp1)
    cp2 = DocumentCopy(document=av1)
    db.session.add(cp2)
avs.append(av1)

av1 = AVMaterial.query.filter(AVMaterial.title == 'The Black Album').first()
if av1 is None:
    av1 = AVMaterial(
        title='The Black Album',
        price=250,
        keywords=['metal', 'music'],
        authors=['Metallica']
    )
    db.session.add(av1)
if DocumentCopy.query.filter(DocumentCopy.document_id == av1.id).count() < 2:
    cp1 = DocumentCopy(document=av1)
    db.session.add(cp1)
    cp2 = DocumentCopy(document=av1)
    db.session.add(cp2)
avs.append(av1)

av1 = AVMaterial.query.filter(AVMaterial.title == 'Good Company').first()
if av1 is None:
    av1 = AVMaterial(
        title='Good Company',
        price=250,
        keywords=['swing', 'music'],
        authors=['Brock Berrigan']
    )
    db.session.add(av1)
if DocumentCopy.query.filter(DocumentCopy.document_id == av1.id).count() < 2:
    cp1 = DocumentCopy(document=av1)
    db.session.add(cp1)
    cp2 = DocumentCopy(document=av1)
    db.session.add(cp2)
avs.append(av1)

articles = []

ar1 = JournalArticle.query.filter(JournalArticle.title == 'Go to Statement Considered Harmful').first()
if ar1 is None:
    ar1 = JournalArticle(
        title='Go to Statement Considered Harmful',
        price=125,
        keywords=['goto', 'programming', 'acm'],
        authors=['Edsger W. Dijkstra'],
        journal='Communication ACM',
        issue_publication_date=datetime.date(1968, 3, 1),
        issue_editor='Edward Nash Yourdon'
    )
    db.session.add(ar1)
if DocumentCopy.query.filter(DocumentCopy.document_id == ar1.id).count() < 2:
    cp1 = DocumentCopy(document=ar1)
    db.session.add(cp1)
    cp2 = DocumentCopy(document=ar1)
    db.session.add(cp2)

if Loan.query.filter(Loan.user == ionagamed).count() < 3:
    for loan in Loan.query.all():
        db.session.delete(loan)
    ionagamed.checkout(books[0].copies[0])
    ionagamed.checkout(books[1].copies[0])
    ionagamed.checkout(books[2].copies[0])
    loan = Loan.query.filter(Loan.document_copy == books[1].copies[0]).first()
    loan.due_date = datetime.date(1990, 1, 1)
    for loan in Loan.query.all():
        loan.status = Loan.Status.approved
        db.session.add(loan)
    loan = Loan.query.filter(Loan.document_copy == books[2].copies[0]).first()
    loan.status = Loan.Status.requested

    ionagamed.checkout(ar1.copies[0])
    loan = Loan.query.filter(Loan.document_copy == ar1.copies[0]).first()
    loan.status = Loan.Status.returned
    db.session.add(loan)

db.session.commit()
