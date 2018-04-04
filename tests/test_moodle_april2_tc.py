from freezegun import freeze_time
import datetime

import pytest

from hexagonal import db, FacultyPatron
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal import Librarian, AVMaterial
from hexagonal.model.student_patron import StudentPatron
from hexagonal import User, Loan, Patron, QueuedRequest, Professor
from hexagonal.model.visiting_professor_patron import VisitingProfessorPatron



def state_of_system():
    d1 = create_instance(Book, title='Introduction to Algorithms',
                         authors=['Thomas H. Cormen', 'Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
                         publisher='MIT Press', publishment_year=2009, edition=3,
                         reference=False, price=5000)

    d2 = create_instance(Book, title='Design Patterns: Elements of Reusable Object-Oriented Software',
                         authors=['Erich Gamma', 'Ralph Johnson', 'John Vlissides', 'Richard Helm'],
                         publisher='Addison-Wesley Professional', publishment_year=2003, edition=1,
                         reference=False, price=1700, bestseller=True)

    d3 = create_instance(Book, title='Null References: The Billion Dollar Mistake',
                         authors=['Tony Hoare'],
                         price=700)

    copies_d1 = [create_instance(DocumentCopy, document=d1) for i in range(3)]
    copies_d2 = [create_instance(DocumentCopy, document=d2) for i in range(3)]
    copies_d3 = [create_instance(DocumentCopy, document=d3) for i in range(2)]

    p1 = register_test_account(Professor, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                               card_number=1010)
    p2 = register_test_account(Professor, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
                               card_number=1011)
    p3 = register_test_account(Professor, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
                               card_number=1100)
    s = register_test_account(StudentPatron, name='Andrey Velo', address=': Avenida Mazatlan 250', phone='30004',
                              card_number=1101)
    v = register_test_account(VisitingProfessorPatron, name='Veronika Rama', address='Stret Atocha, 27', phone='30005',
                              card_number=1110)
    docs_set = [copies_d1, copies_d2, copies_d3, d1, d2, d3]
    users_set_patrons = [p1, p2, p3]
    users_set_students = [s]
    users_set_visiting_profs = [v]

    return docs_set, users_set_patrons, users_set_students, users_set_visiting_profs


def test_tc1__patron_checkout_a_document_and_doc_is_not_overdued():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    d1_copies = documents[0]
    d2_copies = documents[1]

    with freeze_time('March 5th, 2018'):
        loan_p1_d1 = p1.checkout(d1_copies[0])
        loan_p1_d2 = p1.checkout(d2_copies[0])

    db.session.delete(loan_p1_d2)
    db.session.commit()

    with freeze_time('April 2nd, 2018'):
        overdued_docs_of_p1 = p1.get_overdue_loans()
        overdued_fine_of_p1_by_d1 = loan_p1_d1.get_overdue_fine()

    assert len(overdued_docs_of_p1) == 0 and overdued_fine_of_p1_by_d1 == 0


def test_tc2_patron_check_out_some_docs_and_some_of_them_are_overdued():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    s = students[0]
    v = visiting_profs[0]

    d1_copies = documents[0]
    d2_copies = documents[1]

    with freeze_time('March 5th, 2018'):
        loan_p1_d1 = p1.checkout(d1_copies[0])
        loan_p1_d1.status = Loan.Status.approved

        loan_p1_d2 = p1.checkout(d2_copies[0])
        loan_p1_d2.status = Loan.Status.approved

        loan_s_d1 = s.checkout(d1_copies[1])
        loan_s_d1.status = Loan.Status.approved

        loan_s_d2 = s.checkout(d2_copies[1])
        loan_s_d2.status = Loan.Status.approved

        loan_v_d1 = v.checkout(d1_copies[2])
        loan_v_d1.status = Loan.Status.approved

        loan_v_d2 = v.checkout(d2_copies[2])
        loan_v_d2.status = Loan.Status.approved

    with freeze_time('April 2nd, 2018'):
        p1_overdued_docs = p1.get_overdue_loans()
        p1_fines = [loan_p1_d1.get_overdue_fine(), loan_p1_d2.get_overdue_fine()]

        s_overdued_docs = s.get_overdue_loans()
        s_fines = [loan_s_d1.get_overdue_fine(), loan_s_d2.get_overdue_fine()]

        v_overdued_docs = v.get_overdue_loans()
        v_fines = [loan_v_d1.get_overdue_fine(), loan_v_d2.get_overdue_fine()]

        assert len(p1_overdued_docs) == 0

        assert len(s_overdued_docs) == 2

        assert s_overdued_docs[0].overdue_days() == 7
        assert s_overdued_docs[0].get_overdue_fine() == 700

        assert s_overdued_docs[1].overdue_days() == 14
        assert s_overdued_docs[1].get_overdue_fine() == 1400

        assert len(v_overdued_docs) == 2

        assert v_overdued_docs[0].overdue_days() == 21
        assert v_overdued_docs[0].get_overdue_fine() == 2100

        assert v_overdued_docs[0].overdue_days() == 21
        assert v_overdued_docs[1].get_overdue_fine() == 1700


def test_tc3_patron_check_out_some_docs_and_due_date_is_correct():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    s = students[0]
    v = visiting_profs[0]

    d1_copies = documents[0]
    d2_copies = documents[1]

    with freeze_time('March 29th, 2018'):
        loan_p1_d1 = p1.checkout(d1_copies[0])
        loan_p1_d1.status = Loan.Status.approved
        loan_s_d2 = s.checkout(d2_copies[0])
        loan_s_d2.status = Loan.Status.approved
        loan_v_d2 = v.checkout(d2_copies[1])
        loan_v_d2.status = Loan.Status.approved

    with freeze_time('April 2nd, 2018'):
        loan_p1_d1.renew_document()
        loan_s_d2.renew_document()
        loan_v_d2.renew_document()

    p1_docs = p1.get_borrowed_document_copies()
    s_docs = s.get_borrowed_document_copies()
    v_docs = v.get_borrowed_document_copies()

    assert p1_docs[0] == d1_copies[0]
    assert loan_p1_d1.due_date == datetime.date(2018, 4, 30)
    assert s_docs[0] == d2_copies[0]
    assert loan_s_d2.due_date == datetime.date(2018, 4, 16)
    assert v_docs[0] == d2_copies[1]
    assert loan_v_d2.due_date == datetime.date(2018, 4, 9)

def test_tc4_patrons_checkout_docs_and_due_date_is_correct():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    s = students[0]
    v = visiting_profs[0]

    d1_copies = documents[0]
    d2_copies = documents[1]

    with freeze_time('March 29th, 2018'):
        loan_p1_d1 = p1.checkout(d1_copies[0])
        loan_p1_d1.status = Loan.Status.approved
        loan_s_d2 = s.checkout(d2_copies[0])
        loan_s_d2.status = Loan.Status.approved
        loan_v_d2 = v.checkout(d2_copies[1])
        loan_v_d2.status = Loan.Status.approved

    with freeze_time('April 2nd, 2018'):
        documents[4].outstanding_request()
        loan_p1_d1.renew_document()
        with pytest.raises(ValueError):
            loan_s_d2.renew_document()
            loan_v_d2.renew_document()

    p1_docs = p1.get_borrowed_document_copies()
    s_docs = s.get_borrowed_document_copies()
    v_docs = v.get_borrowed_document_copies()

    assert p1_docs[0] == d1_copies[0]
    assert loan_p1_d1.due_date == datetime.date(2018, 4, 30)
    assert s_docs[0] == d2_copies[0]
    assert loan_s_d2.due_date == datetime.date(2018, 4, 2)
    assert v_docs[0] == d2_copies[1]
    assert loan_v_d2.due_date == datetime.date(2018, 4, 2)

def test_tc5_waiting_list_with_1_user_is_correct():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    s = students[0]
    v = visiting_profs[0]

    d3_copies = documents[2]

    loan_p1_d3 = p1.checkout(d3_copies[0])
    loan_p1_d3.status = Loan.Status.approved
    loan_s_d3 = s.checkout(d3_copies[1])
    loan_s_d3.status = Loan.Status.approved

    qr_v_d3 = QueuedRequest(
        patron=v,
        document=documents[5]
    )
    db.session.add(qr_v_d3)
    db.session.commit()

    waiting_list = QueuedRequest.query.order_by(QueuedRequest.created_at).all()
    waiting_list = sorted(waiting_list, key=lambda x: (x.priority, x.created_at))

    assert len(waiting_list) == 1
    assert waiting_list[0].patron.id == v.id


def test_tc6_waiting_list_with_3_users_is_correct():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    p2 = patrons[1]
    p3 = patrons[2]
    s = students[0]
    v = visiting_profs[0]

    d3_copies = documents[2]

    loan_p1_d3 = p1.checkout(d3_copies[0])
    loan_p1_d3.status = Loan.Status.approved
    loan_p2_d3 = p2.checkout(d3_copies[1])
    loan_p2_d3.status = Loan.Status.approved

    qr_s_d3 = QueuedRequest(
        patron=s,
        document=documents[5]
    )
    db.session.add(qr_s_d3)
    qr_v_d3 = QueuedRequest(
        patron=v,
        document=documents[5]
    )
    db.session.add(qr_v_d3)
    qr_p3_d3 = QueuedRequest(
        patron=p3,
        document=documents[5]
    )
    db.session.add(qr_p3_d3)

    db.session.commit()

    waiting_list = QueuedRequest.query.order_by(QueuedRequest.created_at).all()
    waiting_list = sorted(waiting_list, key=lambda x: (x.priority, x.created_at))

    assert waiting_list[0].patron == s
    assert waiting_list[1].patron == v
    assert waiting_list[2].patron == p3

def test_tc7_():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    p2 = patrons[1]
    p3 = patrons[2]
    s = students[0]
    v = visiting_profs[0]

    d3_copies = documents[2]

    loan_p1_d3 = p1.checkout(d3_copies[0])
    loan_p1_d3.status = Loan.Status.approved
    loan_p2_d3 = p2.checkout(d3_copies[1])
    loan_p2_d3.status = Loan.Status.approved

    qr_s_d3 = QueuedRequest(
        patron=s,
        document=documents[5]
    )
    db.session.add(qr_s_d3)
    qr_v_d3 = QueuedRequest(
        patron=v,
        document=documents[5]
    )
    db.session.add(qr_v_d3)
    qr_p3_d3 = QueuedRequest(
        patron=p3,
        document=documents[5]
    )
    db.session.add(qr_p3_d3)

    db.session.commit()

    d3 = documents[5]
    d3.outstanding_request()

    waiting_list = QueuedRequest.query.order_by(QueuedRequest.created_at).all()
    waiting_list = sorted(waiting_list, key=lambda x: (x.priority, x.created_at))

    assert len(waiting_list) == 0
    # p1 and p2 notified that they should return books
    # s, v, p1 notified that d3 is no longer available

def tests_tc8_notificatioin_about_availibility_of_d3_book_from_waiting_list():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    p2 = patrons[1]
    p3 = patrons[2]
    s = students[0]
    v = visiting_profs[0]

    d3_copies = documents[2]

    loan_p1_d3 = p1.checkout(d3_copies[0])
    loan_p1_d3.status = Loan.Status.approved
    loan_p2_d3 = p2.checkout(d3_copies[1])
    loan_p2_d3.status = Loan.Status.approved

    # # # мм та часть в которой у нас все должно работать
    # # loan_s_d3 = s.checkout(d3_copies)
    # # loan_v_d3 = v.checkout(d3_copies)
    # # loan_p3_d3 = p3.checkout(d3_copies)

    # db.session.delete(loan_p2_d3)
    # db.session.commit()
    # s is notified about d3

    # assert p2.get_loans() == []
    # # assert waiting_list == [s,v,p3]

def test_tc9_():
    reload_db()
    documents, patrons, students, visiting_profs = state_of_system()

    p1 = patrons[0]
    p2 = patrons[1]
    p3 = patrons[2]
    s = students[0]
    v = visiting_profs[0]

    d3_copies = documents[2]

    loan_p1_d3 = p1.checkout(d3_copies[0])
    loan_p1_d3.status = Loan.Status.approved
    loan_p2_d3 = p2.checkout(d3_copies[1])
    loan_p2_d3.status = Loan.Status.approved

    qr_s_d3 = QueuedRequest(
        patron=s,
        document=documents[5]
    )
    db.session.add(qr_s_d3)
    qr_v_d3 = QueuedRequest(
        patron=v,
        document=documents[5]
    )
    db.session.add(qr_v_d3)
    qr_p3_d3 = QueuedRequest(
        patron=p3,
        document=documents[5]
    )
    db.session.add(qr_p3_d3)

    db.session.commit()

    waiting_list = QueuedRequest.query.order_by(QueuedRequest.created_at).all()
    waiting_list = sorted(waiting_list, key=lambda x: (x.priority, x.created_at))

    with freeze_time('April 2nd, 2018'):
        loan_p1_d3.renew_document()

    assert loan_p1_d3.due_date == datetime.date(2018, 4, 30)
    assert loan_p1_d3.document_copy == d3_copies[0]
    assert waiting_list[0].patron == s
    assert waiting_list[1].patron == v
    assert waiting_list[2].patron == p3

# def test_tc10_():
#     reload_db()
#     documents, patrons, students, visiting_profs = state_of_system()
#
#     p1 = patrons[0]
#     p2 = patrons[1]
#     p3 = patrons[2]
#     s = students[0]
#     v = visiting_profs[0]
#
#     d1_copies = documents[0]
#     d3_copies = documents[2]
#
#     datetime.today = datetime.date(2018, 3, 26)
#     loan_p1_d1 = p1.checkout(d1_copies[0])
#     loan_p1_d1.status = Loan.Status.approved
#     loan_v_d1 = v.checkout(d1_copies[1])
#     loan_v_d1.status = Loan.Status.approved
#
#     datetime.today = datetime.date(2018,3,29)
#     loan_p1_d1.renew_document()
#     loan_v_d1.renew_document()
#
#     datetime.today = datetime.date(2018,4,2)
#     loan_p1_d1.renew_document()
#     loan_v_d1.renew_document()
#
#     assert loan_p1_d1.document_copy == d1_copies[0] and loan_p1_d1.due_date == datetime.date(2018, 4, 26)
#     assert loan_v_d1.document_copy == d1_copies[1] and loan_v_d1.due_date == datetime.date(2018, 4, 5)
