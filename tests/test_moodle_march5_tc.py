import datetime

import pytest

from hexagonal import db, FacultyPatron
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal import Librarian, AVMaterial
from hexagonal.model.student_patron import StudentPatron
from hexagonal import User, Loan, Patron


# def create_a_system_of_first_test_state():
#     b1 = create_instance(Book, title='Introduction to Algorithms',
#                          authors=['Thomas H. Cormen', ' Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
#                          publisher='MIT Press', publishment_year=2009, edition=3)
#     copies = [create_instance(DocumentCopy, document=b1) for i in range(3)]
#
#     b2 = create_instance(Book, title='Design Patterns: Elements of Reusable Object-Oriented Software',
#                          authors=['Erich Gamma', 'Ralph Johnson', ' John Vlissides', 'Richard Helm'],
#                          publisher='Addison-Wesley Professional', publishment_year=2003, edition=1, bestseller=True)
#     copies_b2 = [create_instance(DocumentCopy, document=b2) for i in range(2)]
#
#     b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
#                          publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
#                          reference=True)
#     copies_b3 = [create_instance(DocumentCopy, document=b3)]
#
#     av1 = create_instance(AVMaterial, title='Null References: The Billion Dollar Mistake', authors='Tony Hoare')
#     av1_copy = [create_instance(DocumentCopy, document=av1)]
#     av2 = create_instance(AVMaterial, title='NInformation Entropy', authors='Claude Shannon')
#     av2_copy = [create_instance(DocumentCopy, document=av2)]
#
#     p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
#                                card_number=1010)
#     p2 = register_test_account(StudentPatron, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
#                                card_number=1011)
#     p3 = register_test_account(StudentPatron, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
#                                card_number=1100)
#     docs_set = [copies, copies_b2, copies_b3, av1_copy, av2_copy, b1, b2, b3, av1, av2]
#     users_set = [p1, p2, p3]
#
#     return docs_set, users_set
#
#
# def create_a_system_of_the_second_state():
#     docs, users = create_a_system_of_first_test_state()
#
#     copies = docs[0]
#     copies_b2 = docs[1]
#
#     db.session.delete(copies[0])
#     db.session.delete(copies[1])
#     db.session.delete(copies_b2[0])
#     db.session.delete(users[1])
#     db.session.commit()
#
#     return docs, users
#
#
# def approve_all_loans():
#     for loan in Loan.query.all():
#         loan.status = Loan.Status.approved
#         db.session.add(loan)
#     db.session.commit()
#
#
# def test_tc1__created_document_copies():
#     reload_db()
#     create_a_system_of_first_test_state()
#     assert DocumentCopy.query.count() == 8 and User.query.count() == 4
#
#
# def test_tc2_documents_in_system_are_5_after_removing():
#     reload_db()
#
#     create_a_system_of_the_second_state()
#
#     assert DocumentCopy.query.count() == 5 and User.query.count() == 3
#
#
# def test_tc3_librarian_checks_and_returned_information_is_right():
#     reload_db()
#
#     create_a_system_of_first_test_state()
#
#     p1_instance = User.query.filter(User.name == 'Sergey Afonso').first()
#     p3_instance = User.query.filter(User.name == 'Elvira Espindola').first()
#
#     assert p1_instance.name == 'Sergey Afonso'
#     assert p3_instance.name == 'Elvira Espindola'
#     assert p1_instance.address == 'Via Margutta, 3'
#     assert p3_instance.address == 'Via del Corso, 22'
#     assert p1_instance.phone == '30001'
#     assert p3_instance.phone == '30003'
#     assert p1_instance.card_number == '1010'
#     assert p3_instance.card_number == '1100'
#
#
# def test_tc4_librarian_checks_informartion_of_already_deleted_and_existing_users():
#     reload_db()
#     create_a_system_of_the_second_state()
#     p2_instance = User.query.filter(User.name == 'Nadia Teixeira').first()
#     p3_instance = User.query.filter(User.name == 'Elvira Espindola').first()
#
#     assert p2_instance is None
#     assert p3_instance.name == 'Elvira Espindola'
#     assert p3_instance.address == 'Via del Corso, 22'
#     assert p3_instance.phone == '30003'
#     assert p3_instance.card_number == '1100'
#     assert isinstance(p3_instance, StudentPatron)
#
#
# def test_tc5_deleted_patron_checkin_out_a_book_and_fails():
#     reload_db()
#     docs, users = create_a_system_of_the_second_state()
#     book1_copy_set = docs[0]
#     patron = User.query.filter(User.name == 'Nadia Teixeira').first()
#
#     with pytest.raises(AttributeError):
#         patron.checkout(book1_copy_set[0])
#     assert patron is None
#
#
# def test_tc6_patrons_checking_out_books_and_all_information_is_right():
#     reload_db()
#
#     b1 = create_instance(Book, title='Introduction to Algorithms',
#                          authors=['Thomas H. Cormen', ' Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
#                          publisher='MIT Press', publishment_year=2009, edition=3)
#     copies_b1 = [create_instance(DocumentCopy, document=b1) for i in range(3)]
#
#     b2 = create_instance(Book, title='Design Patterns: Elements of Reusable Object-Oriented Software',
#                          authors=['Erich Gamma', 'Ralph Johnson', ' John Vlissides', 'Richard Helm'],
#                          publisher='Addison-Wesley Professional', publishment_year=2003, edition=1, bestseller=True)
#     copies_b2 = [create_instance(DocumentCopy, document=b2) for i in range(2)]
#
#     b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
#                          publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
#                          reference=True)
#     copies_b3 = create_instance(DocumentCopy, document=b3)
#
#     av1 = create_instance(AVMaterial, title='Null References: The Billion Dollar Mistake', authors='Tony Hoare')
#     av1_copy = create_instance(DocumentCopy, document=av1)
#     av2 = create_instance(AVMaterial, title='NInformation Entropy', authors='Claude Shannon')
#     av2_copy = create_instance(DocumentCopy, document=av2)
#
#     p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
#                                card_number=1010)
#     p2 = register_test_account(StudentPatron, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
#                                card_number=1011)
#     p3 = register_test_account(StudentPatron, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
#                                card_number=1100)
#
#     db.session.delete(copies_b1[0])
#     db.session.delete(copies_b1[1])
#     db.session.delete(copies_b2[0])
#     db.session.delete(p2)
#     db.session.commit()
#
#     # users, docs = create_a_system_of_the_second_state()
#     # p1 = users[0]
#     # p3 = users[2]
#     # copies_b1 = docs[0]
#     # copies_b2 = docs[1]
#
#     p1_b1_loan = p1.checkout(copies_b1[2])
#     p3_b2_loan = p3.checkout(copies_b2[1])
#
#     assert p1.name == 'Sergey Afonso'
#     assert p3.name == 'Elvira Espindola'
#     assert p1.address == 'Via Margutta, 3'
#     assert p3.address == 'Via del Corso, 22'
#     assert p1.phone == '30001'
#     assert p3.phone == '30003'
#     assert p1.card_number == '1010'
#     assert p3.card_number == '1100'
#     assert p1_b1_loan.document_copy == copies_b1[2]
#     assert p3_b2_loan.document_copy == copies_b2[1]
#     assert p1_b1_loan.due_date == datetime.date(2018, 4, 4)
#     assert p3_b2_loan.due_date == datetime.date(2018, 3, 21)
#
#
# def test_tc7_patrons_checing_out_books_and_return_date_is_right():
#     reload_db()
#     docs, users = create_a_system_of_first_test_state()
#     p1 = users[0]
#     p2 = users[1]
#     book1_copies = docs[0]
#     book2_copies = docs[1]
#     book3_copies = docs[2]
#     av1_copies = docs[3]
#     av2_copies = docs[4]
#
#     p1.checkout(book1_copies[0])
#     p1.checkout(book2_copies[0])
#     with pytest.raises(ValueError):
#         p1.checkout(book3_copies[0])
#     p1.checkout(av1_copies[0])
#     p2.checkout(book1_copies[1])
#     p2.checkout(book2_copies[1])
#     p2.checkout(av2_copies[0])
#
#     approve_all_loans()
#
#     p1_docs = list(map(
#         lambda x: (x.document.id, x.loan.due_date),
#         p1.get_borrowed_document_copies()
#     ))
#
#     p2_docs = list(map(
#         lambda x: (x.document.id, x.loan.due_date),
#         p2.get_borrowed_document_copies()
#     ))
#
#     assert set(p1_docs) == {
#         (
#             docs[5].id,
#             datetime.date.today() + datetime.timedelta(weeks=4)
#         ),
#         (
#             docs[6].id,
#             datetime.date.today() + datetime.timedelta(weeks=4)
#         ),
#         (
#             docs[8].id,
#             datetime.date.today() + datetime.timedelta(weeks=2)
#         )
#     }
#
#     assert set(p2_docs) == {
#         (
#             docs[5].id,
#             datetime.date.today() + datetime.timedelta(weeks=3)
#         ),
#         (
#             docs[6].id,
#             datetime.date.today() + datetime.timedelta(weeks=2)
#         ),
#         (
#             docs[9].id,
#             datetime.date.today() + datetime.timedelta(weeks=2)
#         )
#     }
#
#
# # def test_tc8_checking_is_date_of_overduing_right():
# #     docs, users = create_a_system_of_first_test_state()
# #     p1 = users[0]
# #     p2 = users[1]
# #     book1_copies = docs[0]
# #     book2_copies = docs[1]
# #     book3_copies = docs[2]
# #     av1_copies = docs[3]
# #     av2_copies = docs[4]
# #
# #     p1.checkout(book1_copies[0])
# #     p1.checkout(book2_copies[0])
# #     with pytest.raises(ValueError):
# #         p1.checkout(book3_copies[0])
# #     p1.checkout(av1_copies[0])
# #     p2.checkout(book1_copies[1])
# #     p2.checkout(book2_copies[1])
# #     p2.checkout(av2_copies[0])
# #
# #     p1_docs = list(map(
# #         lambda x: (x.document.id, x.due_date),
# #         p1.get_borrowed_documents()
# #     ))
# #
# #     p2_docs = list(map(
# #         lambda x: (x.document.id, x.due_date),
# #         p2.get_borrowed_documents()
# #     ))
# #
# #     print(p1_docs)
# #
# #     assert p1_docs == [
# #         (
# #             book1_copies[5].id,
# #         )
# #     ]
#
#
# def test_tc8_checking_is_date_of_overduing_right():
#     reload_db()
#     b1 = create_instance(Book, title='Introduction to Algorithms',
#                          authors=['Thomas H. Cormen', ' Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
#                          publisher='MIT Press', publishment_year=2009, edition=3)
#     copies_b1 = [create_instance(DocumentCopy, document=b1) for i in range(3)]
#
#     b2 = create_instance(Book, title='Design Patterns: Elements of Reusable Object-Oriented Software',
#                          authors=['Erich Gamma', 'Ralph Johnson', ' John Vlissides', 'Richard Helm'],
#                          publisher='Addison-Wesley Professional', publishment_year=2003, edition=1, bestseller=True)
#     copies_b2 = [create_instance(DocumentCopy, document=b2) for i in range(2)]
#
#     b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
#                          publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
#                          reference=True)
#     copies_b3 = [create_instance(DocumentCopy, document=b3)]
#
#     av1 = create_instance(AVMaterial, title='Null References: The Billion Dollar Mistake', authors='Tony Hoare')
#     av1_copy = [create_instance(DocumentCopy, document=av1)]
#     av2 = create_instance(AVMaterial, title='NInformation Entropy', authors='Claude Shannon')
#     av2_copy = [create_instance(DocumentCopy, document=av2)]
#
#     p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
#                                card_number=1010)
#     p2 = register_test_account(StudentPatron, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
#                                card_number=1011)
#     p3 = register_test_account(StudentPatron, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
#                                card_number=1100)
#
#     loan_p1_b1 = p1.checkout(copies_b1[0])
#
#     loan_p1_b1.due_date = datetime.date(2018, 2, 9) + (loan_p1_b1.due_date - datetime.date.today())
#     loan_p1_b2 = p1.checkout(copies_b2[0])
#     loan_p1_b2.due_date = datetime.date(2018, 2, 2) + (loan_p1_b2.due_date - datetime.date.today())
#     loan_p2_b1 = p2.checkout(copies_b1[1])
#     loan_p2_b1.due_date = datetime.date(2018, 2, 5) + (loan_p2_b1.due_date - datetime.date.today())
#     loan_p2_av1 = p2.checkout(av1_copy[0])
#     loan_p2_av1.due_date = datetime.date(2018, 2, 17) + (loan_p2_av1.due_date - datetime.date.today())
#
#     assert loan_p1_b2.overdue_days() - 0 == 5 and loan_p2_b1.overdue_days() - 0 == 9 and loan_p2_av1.overdue_days() - 0 == 4

def test_9_renew_is_working():
    reload_db()
    b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
                         publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
                         reference=False)
    copies_b3 = [create_instance(DocumentCopy, document=b3)]
    p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                               card_number=1010)
    loan_p1_b3 = p1.checkout(copies_b3[0])
    loan_p1_b3.due_date = datetime.date(2018, 2, 9)
    old_date = loan_p1_b3.due_date
    loan_p1_b3.renew_document()

    renewed_date = loan_p1_b3.due_date

    assert old_date != renewed_date
