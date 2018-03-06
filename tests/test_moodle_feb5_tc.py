import datetime

import pytest

from hexagonal import db, FacultyPatron
#from hexagonal.functions.book import create_book
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.student_patron import StudentPatron
#from hexagonal.model.author import Author
# from hexagonal.functions import Book

#
# def test_tc1__librarian_can_see_checked_out_items():
#     reload_db()
#
#     root_token = root_login()
#     patron = register_test_account(StudentPatron)
#
#     book_id = call(
#         'book.create',
#         {
#             'title': 'One Big Book',
#             'edition': '1',
#             'author_names': ['123'],
#             'publisher_name': '345'
#         },
#         root_token
#     )
#
#     book_copy_1 = create_instance(DocumentCopy, document_id=book_id[id])
#     create_instance(DocumentCopy, document=book_id['id'])
#
#     patron.checkout(book_copy_1)
#
#     l = call(
#         'user.get_borrowed_copies',
#         [patron.id],
#         token=root_token
#     )
#
#     assert list(map(lambda x: x['id'], l)) == [book_copy_1.id]
#
#
# def test_tc1__librarian_can_see_available_items():
#     reload_db()
#
#     root_token = root_login()
#     patron = register_test_account(StudentPatron)
#     book = create_instance(Book, title='Two Big Books', edition=1)
#     book_copy_1 = create_instance(DocumentCopy, document=book)
#     book_copy_2 = create_instance(DocumentCopy, document=book)
#
#     patron.checkout(book_copy_1)
#
#     l = call(
#         'get_available_document_copies',
#         [],
#         token=root_token
#     )
#
#     assert list(map(lambda x: x['id'], l)) == [book_copy_2.id]
#

# def test_tc2_patron_cant_check_out_book_by_author_a():
#     reload_db()
#
#     # root_token = root_login()
#     patron = register_test_account(StudentPatron)
#     book_author = create_instance(Author, name='Bertrand Mayer')
#     book = create_instance(Book, title='Touch of class', authors=[book_author])
#
#     with pytest.raises(IndexError):
#         patron.checkout(book.copies[0])
#
#
# def test_tc3__faculty_patron_checks_out_for_4_weeks():
#     reload_db()
#
#     patron = register_test_account(FacultyPatron)
#     book = create_instance(Book, title='One Big Book', edition=1)
#     book_copy = create_instance(DocumentCopy, document=book)
#
#     loan = patron.checkout(book_copy)
#
#     assert (loan.due_date - datetime.date.today()).days == 28
#
#
# def test_tc4__faculty_patron_checks_out_bestseller_for_2_weeks():
#     reload_db()
#
#     patron = register_test_account(FacultyPatron)
#     book = create_instance(Book, title='Second Big Book', edition=2, bestseller=True)
#     book_copy = create_instance(DocumentCopy, document=book)
#
#     loan = patron.checkout(book_copy)
#
#     assert (loan.due_date - datetime.date.today()).days == 28
#
#
# def test_tc5__3_patrons_check_out_2_books_should_fail():
#     reload_db()
#
#     patrons = [register_test_account(StudentPatron) for i in range(3)]
#     book = create_instance(Book, title='One Big Book', edition=1)
#     copies = [create_instance(DocumentCopy, document=book) for i in range(2)]
#
#     patrons[0].checkout(copies[0])
#     patrons[1].checkout(copies[1])
#     with pytest.raises(ValueError):
#         patrons[2].checkout(copies[0])
# #
# #
# # def test_tc5__3_patrons_check_out_2_books__and_last_should_not_see_others():
# #     reload_db()
# #
# #     root_token = root_login()
# #     patrons = [register_test_account(StudentPatron) for i in range(3)]
# #     book = create_instance(Book, title='One Big Book', edition=1)
# #     copies = [create_instance(DocumentCopy, document=book) for i in range(2)]
# #
# #     patrons[0].checkout(copies[0])
# #     patrons[1].checkout(copies[1])
# #
# #     l = call(
# #         'get_available_document_copies',
# #         [],
# #         token=root_token
# #     )
# #
# #     assert l == []
# #
# #
# def test_tc8__student_patron_checks_out_book_for_3_weeks():
#     reload_db()
#
#     faculty_patron = register_test_account(FacultyPatron)
#     student_patron = register_test_account(StudentPatron)
#     book = create_instance(Book, title='First Big Book', edition=1)
#     book_copy = create_instance(DocumentCopy, document=book)
#
#     loan = student_patron.checkout(book_copy)
#
#     assert (loan.due_date - datetime.date.today()).days == 21
#
#
# def test_tc9__student_patron_checks_out_bestseller_for_2_weeks():
#     reload_db()
#
#     faculty_patron = register_test_account(FacultyPatron)
#     student_patron = register_test_account(StudentPatron)
#     book = create_instance(Book, title='Second Big Book', edition=2, bestseller=True)
#     book_copy = create_instance(DocumentCopy, document=book)
#
#     loan = student_patron.checkout(book_copy)
#
#     assert (loan.due_date - datetime.date.today()).days == 14
# #
# #
# # def test_tc10_patron_can_check_out_a_book_and_not_available_to_check_out_reference_book():
# #     reload_db()
# #
# #     root_token = root_login()
# #     patron = register_test_account(StudentPatron)
# #     book = create_instance(Book, title='First Big Book')
# #     book_copy = create_instance(DocumentCopy, document=book)
# #     reference_book = create_instance(Book, title='Second Big Reference Book', reference=True)
# #     reference_book_copy = create_instance(DocumentCopy, document=reference_book)
# #
# #     patron.checkout(book_copy)
# #
# #     l = call(
# #         'user.get_borrowed_copies',
# #         [patron.id],
# #         token=root_token
# #     )
# #
# #     assert list(map(lambda x: x['id'], l)) == [book_copy.id]
#
#
# def test_tc10_patron_are_not_available_to_check_out_reference_book():
#     reload_db()
#
#     patron = register_test_account(StudentPatron)
#     reference_book = create_instance(Book, title='One Big Reference Book', reference=True)
#     reference_book_copy = create_instance(DocumentCopy, document=reference_book)
#
#     with pytest.raises(ValueError):
#         patron.checkout(reference_book_copy)
