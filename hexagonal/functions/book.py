from hexagonal import Author, Publisher, db, Book
from hexagonal import jsonrpc
from hexagonal.auth.helpers import minimum_access_level


@jsonrpc.bind('book.create')
@minimum_access_level('librarian')
def create_book(title, edition, author_names, publisher_name, bestseller=False):
    """Function for creating a boo in database system.
        Checking cases when we already have an existing publisher/authors,
            in case if they are not exist, we are adding them to database system
       Creating a book in system, attaching it to already existing parameters as publisher, author
    """

    publisher = Publisher.query.filter(Publisher.name == publisher_name).first()
    if publisher is None:
        publisher = Publisher(name=publisher_name)
        db.session.add(publisher)

    authors = []
    for name in author_names:
        author = Author.query.filter(Author.name == name).first()
        if author is None:
            author = Author(name=name)
            db.session.add(author)
        authors.append(author)

    book = Book(
        title=title,
        edition=edition,
        authors=authors,
        publisher=publisher,
        bestseller=bestseller
    )

    db.session.add(book)
    db.session.commit()

    return book.id


@jsonrpc.bind('book.get')
@minimum_access_level('librarian')
def get_books():
    return list(Book.query.all())
