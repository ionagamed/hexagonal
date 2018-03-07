import datetime

import pytest

from hexagonal import db, FacultyPatron
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal import Librarian, AVMaterial
from hexagonal.model.student_patron import StudentPatron
from hexagonal import User


def create_a_system_of_first_test_state():

    b1 = create_instance(Book, title='Introduction to Algorithms',
                         authors=['Thomas H. Cormen', ' Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
                         publisher='MIT Press', publishment_year=2009, edition=3)
    copies = [create_instance(DocumentCopy, document=b1) for i in range(3)]

    b2 = create_instance(Book, title='Design Patterns: Elements of Reusable Object-Oriented Software',
                         authors=['Erich Gamma', 'Ralph Johnson', ' John Vlissides', 'Richard Helm'],
                         publisher='Addison-Wesley Professional', publishment_year=2003, edition=1, bestseller=True)
    copies_b2 = [create_instance(DocumentCopy, document=b2) for i in range(2)]

    b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
                         publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
                         reference=True)
    copies_b3 = create_instance(DocumentCopy, document=b3)

    av1 = create_instance(AVMaterial, title='Null References: The Billion Dollar Mistake', authors='Tony Hoare')
    av1_copy = create_instance(DocumentCopy, document=av1)
    av2 = create_instance(AVMaterial, title='NInformation Entropy', authors='Claude Shannon')
    av2_copy = create_instance(DocumentCopy, document=av2)

    p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                               card_number=1010)
    p2 = register_test_account(StudentPatron, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
                               card_number=1011)
    p3 = register_test_account(StudentPatron, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
                               card_number=1100)
    docs_set = [copies, copies_b2, copies_b3, av1_copy, av2_copy]
    users_set = [p1, p2, p3]

    return docs_set, users_set


def create_a_system_of_the_second_state():
    docs, users = create_a_system_of_first_test_state()

    copies = docs[0]
    copies_b2 = docs[1]

    db.session.delete(copies[0])
    db.session.delete(copies[1])
    db.session.delete(copies_b2[0])
    db.session.delete(users[1])
    db.session.commit()

    return docs, users


def test_tc1__created_document_copies():
    reload_db()
    create_a_system_of_first_test_state()
    assert DocumentCopy.query.count() == 8 and User.query.count()  == 4


def test_tc2_documents_in_system_are_5_after_removing():
    reload_db()

    create_a_system_of_the_second_state()

    assert DocumentCopy.query.count() == 5 and User.query.count() == 3


def test_tc3_librarian_checks_and_returned_information_is_right():
    reload_db()

    create_a_system_of_first_test_state()

    p1_instance = User.query.filter(User.name == 'Sergey Afonso').first()
    p3_instance = User.query.filter(User.name == 'Elvira Espindola').first()

    if (p1_instance.name == 'Sergey Afonso' and p3_instance.name == 'Elvira Espindola'):
        names_are_right = True
    if p1_instance.address == 'Via Margutta, 3' and p3_instance.address == 'Via del Corso, 22':
        addresses_are_right = True
    if p1_instance.phone == '30001' and p3_instance.phone == '30003':
        phones_are_right = True
    if p1_instance.card_number == '1010' and p3_instance.card_number == '1100':
        card_numbers_are_right = True

    assert names_are_right and addresses_are_right and phones_are_right and card_numbers_are_right


def test_tc4_libraria_checks_informarion_of_already_deleted_and_existing_users():
    reload_db()
    create_a_system_of_the_second_state()
    p2_instance = User.query.filter(User.name == 'Nadia Teixeira').first()
    p3_instance = User.query.filter(User.name == 'Elvira Espindola').first()

    information_of_p3_is_right = False

    if (
            p3_instance.name == 'Elvira Espindola' and p3_instance.address == 'Via del Corso, 22' and p3_instance.phone == '30003' and p3_instance.card_number == '1100' and p3_instance.role == 'student-patron'):
        information_of_p3_is_right = True
    assert information_of_p3_is_right and p2_instance == None

# def test_tc5_deleted_patron_checkin_out_a_book_and_fails():
#     docs, users = create_a_system_of_the_second_state()
#     book1_copy_set = docs[0]
#     patron = User.query.filter(User.name == 'Nadia Teixeira')
#
#     with pytest.raises(ValueError):
#         patron.checkout(book1_copy_set[0])

def test_tc6_patrons_checking_out_books_and_all_information_is_right():

    reload_db()

    b1 = create_instance(Book, title='Introduction to Algorithms',
                         authors=['Thomas H. Cormen', ' Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
                         publisher='MIT Press', publishment_year=2009, edition=3)
    copies_b1 = [create_instance(DocumentCopy, document=b1) for i in range(3)]

    b2 = create_instance(Book, title='Design Patterns: Elements of Reusable Object-Oriented Software',
                         authors=['Erich Gamma', 'Ralph Johnson', ' John Vlissides', 'Richard Helm'],
                         publisher='Addison-Wesley Professional', publishment_year=2003, edition=1, bestseller=True)
    copies_b2 = [create_instance(DocumentCopy, document=b2) for i in range(2)]

    b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
                         publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
                         reference=True)
    copies_b3 = create_instance(DocumentCopy, document=b3)

    av1 = create_instance(AVMaterial, title='Null References: The Billion Dollar Mistake', authors='Tony Hoare')
    av1_copy = create_instance(DocumentCopy, document=av1)
    av2 = create_instance(AVMaterial, title='NInformation Entropy', authors='Claude Shannon')
    av2_copy = create_instance(DocumentCopy, document=av2)

    p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                               card_number=1010)
    p2 = register_test_account(StudentPatron, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
                               card_number=1011)
    p3 = register_test_account(StudentPatron, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
                               card_number=1100)


    p1_b1_loan = p1.checkout(copies_b1[0])
    p3_b1_loan  = p3.checkout(copies_b1[1])

    # здесь должна быть адресация к книге которую взял ПОЛЬЗОВАТЕЛЬ и к дате ее возврата но было 2 экза. мозг устал.
    # а по факту я просто такая ооо книжка хмммм дайте мне дату так так так что тут у нас

    date_of_returning_book_by_p1 = p1_b1_loan.due_date
    date_of_returning_book_by_p3 = p3_b1_loan.due_date


    assert date_of_returning_book_by_p1 == datetime.date(2018, 4, 4) and date_of_returning_book_by_p3 == datetime.date(2018, 3, 28)

#
# def test_tc7_patrons_checing_out_books_and_return_date_is_right():
#     docs, users = create_a_system_of_the_first_state()
#     p1 = users[0]
#     p2 = users[1]
#     book1_copies = docs[0]
#     book2_copies = docs[1]
#     book3_copies = docs[2]
#     av1_copies = docs[3]
#     av2_copies = docs[4]
#     p1.checkout(book1_copies[0])
#     p1.checkout(book2_copies[0])
#     p1.checkout(book3_copies[0])
#     p1.checkout(av1_copies[0])
#     p2.checkout(book1_copies[1])
#     p2.checkout(book2_copies[1])
#     p2.checkout(av2_copies[0])
#
#     assert information_of_boths_are_correct
#
# def test_tc8_checking_is_date_of_overduing_right():
#     docs, users = create_a_system_of_first_test_state()
#     p1 = users[0]
#     p2 = users[1]
#     book1_copies = docs[0]
#     book2_copies = docs[1]
#     book3_copies = docs[2]
#     av1_copies = docs[3]
#     av2_copies = docs[4]
#     p1.checkout(book1_copies[0])
#     book1_copies[0].date_of_checkout = february 9
#     p1.checkout(book2_copies[0])
#     p2.checkout(book1_copies[1])
#     p2.checkout(av1_copies[0])
#     # тратата все такое
#     # здесь еще из patron get overdue period date
#
#     assert p1.overdue[book2_copies[0]] == 4 days (tomorrow will be 5) and p2.overdue[book1_copies[0]] == (8 + 1) and p2.overdue[av1] == 2+1
