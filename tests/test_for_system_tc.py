import datetime

import pytest

from hexagonal import db, FacultyPatron
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal import Librarian, AVMaterial
from hexagonal.model.student_patron import StudentPatron
from hexagonal import User, Loan, Patron
from hexagonal.model.visiting_professor_patron import VisitingProfessorPatron


# def test_renew_is_working():
#     reload_db()
#     b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
#                          publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
#                          reference=False)
#     copies_b3 = [create_instance(DocumentCopy, document=b3)]
#     p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
#                                card_number=1010)
#     loan_p1_b3 = p1.checkout(copies_b3[0])
#     loan_p1_b3.due_date = datetime.date(2018, 2, 9)
#     old_date = loan_p1_b3.due_date
#     loan_p1_b3.renew_document()
#
#     renewed_date = loan_p1_b3.due_date
#
#     assert old_date != renewed_date


def test_visiting_prof_can_checkout_a_book_for_1_week():
    reload_db()
    b3 = create_instance(Book, title='The Mythical Man-month', authors=['Brooks,Jr', 'Frederick P'],
                         publisher='Addison-Wesley Longman Publishing Co., Inc.', publishment_year=1995, edition=2,
                         reference=False)
    copies_b3 = [create_instance(DocumentCopy, document=b3)]
    p1 = register_test_account(VisitingProfessorPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                               card_number=1010)
    loan_p1_b3 = p1.checkout(copies_b3[0])
    today = datetime.date.today()
    give_back_date = loan_p1_b3.due_date

    date_delta = give_back_date - today

    assert date_delta.days == 7
