import datetime

import pytest

from hexagonal import db, FacultyPatron
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.student_patron import StudentPatron


def test_tc1__librarian_can_see_checked_out_items():
    reload_db()

    root_token = root_login()
    patron = register_test_account(StudentPatron)
    book = create_instance(Book, title='One Big Book', edition=1)
    book_copy_1 = create_instance(DocumentCopy, document=book)
    create_instance(DocumentCopy, document=book)

    patron.checkout(book_copy_1)

    l = call(
        'user.get_borrowed_copies',
        [patron.id],
        token=root_token
    )

    assert list(map(lambda x: x['id'], l)) == [book_copy_1.id]


def test_tc1__librarian_can_see_available_items():
    reload_db()

    root_token = root_login()
    patron = register_test_account(StudentPatron)
    book = create_instance(Book, title='Two Big Books', edition=1)
    book_copy_1 = create_instance(DocumentCopy, document=book)
    book_copy_2 = create_instance(DocumentCopy, document=book)

    patron.checkout(book_copy_1)

    l = call(
        'get_available_document_copies',
        [],
        token=root_token
    )

    assert list(map(lambda x: x['id'], l)) == [book_copy_2.id]


def test_tc3__faculty_patron_checks_out_for_4_weeks():
    reload_db()

    patron = register_test_account(FacultyPatron)
    book = create_instance(Book, title='One Big Book', edition=1)
    book_copy = create_instance(DocumentCopy, document=book)

    loan = patron.checkout(book_copy)

    assert (loan.due_date - datetime.date.today()).days == 28


def test_tc4__faculty_patron_checks_out_bestseller_for_2_weeks():
    reload_db()

    patron = register_test_account(FacultyPatron)
    book = create_instance(Book, title='Second Big Book', edition=2, bestseller=True)
    book_copy = create_instance(DocumentCopy, document=book)

    loan = patron.checkout(book_copy)

    assert (loan.due_date - datetime.date.today()).days == 28



def test_tc5__3_patrons_check_out_2_books_should_fail():
    reload_db()

    patrons = [register_test_account(StudentPatron) for i in range(3)]
    book = create_instance(Book, title='One Big Book', edition=1)
    copies = [create_instance(DocumentCopy, document=book) for i in range(2)]

    patrons[0].checkout(copies[0])
    patrons[1].checkout(copies[1])
    with pytest.raises(ValueError):
        patrons[2].checkout(copies[0])


def test_tc5__3_patrons_check_out_2_books__and_last_should_not_see_others():
    reload_db()

    root_token = root_login()
    patrons = [register_test_account(StudentPatron) for i in range(3)]
    book = create_instance(Book, title='One Big Book', edition=1)
    copies = [create_instance(DocumentCopy, document=book) for i in range(2)]

    patrons[0].checkout(copies[0])
    patrons[1].checkout(copies[1])

    l = call(
        'get_available_document_copies',
        [],
        token=root_token
    )

    assert l == []


# def test_tc7__2_patrons_check_out_2_copies_of_a_book__system_should_track():
#     reload_db()
#
#     root_token = root_login()
#     patrons = [register_test_account(StudentPatron) for i in range (2)]
#     book = create_instance(Book, title ='One Big Book', edition = 1)
#     copies = [create_instance(DocumentCopy,document = book) for i in range (2)]
#
#     patrons[0].checkout(copies[0])
#     patrons[1].checkout(copies[1])
#
#     l = call(
#         'user.get_borrowed_copies',
#         [patrons[0].id],
#         token=root_token
#     )
#
#     k = call(
#         'user.get_borrowed_copies',
#         [patrons[1].id],
#         token=root_token
#     )
#
#     assert list(map(lambda x: x['id'], l)) == [copies[0].id] and list(map(lambda x: x['id'], k)) == [copies[1].id]

def test_tc8__student_patron_checks_out_book_for_3_weeks():
    reload_db()

    faculty_patron = register_test_account(FacultyPatron)
    student_patron = register_test_account(StudentPatron)
    book = create_instance(Book, title='First Big Book', edition=1)
    book_copy = create_instance(DocumentCopy, document=book)

    loan = student_patron.checkout(book_copy)

    assert (loan.due_date - datetime.date.today()).days == 21

def test_tc9__student_patron_checks_out_bestseller_for_2_weeks():
    reload_db()

    faculty_patron = register_test_account(FacultyPatron)
    student_patron = register_test_account(StudentPatron)
    book = create_instance(Book, title='Second Big Book', edition=2, bestseller=True)
    book_copy = create_instance(DocumentCopy, document=book)

    loan = student_patron.checkout(book_copy)

    assert (loan.due_date - datetime.date.today()).days == 14



