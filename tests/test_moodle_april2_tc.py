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

    p1 = register_test_account(FacultyPatron, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                               card_number=1010)
    p2 = register_test_account(FacultyPatron, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
                               card_number=1011)
    p3 = register_test_account(FacultyPatron, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
                               card_number=1100)
    s = register_test_account(StudentPatron, name='Andrey Velo', address=': Avenida Mazatlan 250', phone='30004',
                              card_number=1101)
    v = register_test_account(VisitingProfessorPatron, name='Veronika Rama', address='Stret Atocha, 27', phone='30005',
                              card_number=1110)
    docs_set = [copies_d1, copies_d2, copies_d3]
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

    datetime.date(2018, 2, 17)
    datetime.today = datetime.date(2018, 3, 5)
    loan_p1_d1 = p1.checkout(d1_copies[0])
    loan_p1_d2 = p1.checkout(d2_copies[0])
    datetime.today = datetime.date(2018, 4, 2)
    db.session.delete(loan_p1_d2)
    db.session.commit()

    docs_of_p1 = p1.get_borrowed_document_copies()

    assert len(docs_of_p1) == 0

# def test_tc2_patron_check_out_some_docs_and_some_of_them_are_overdued():
