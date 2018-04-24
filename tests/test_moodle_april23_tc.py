from freezegun import freeze_time
import datetime

import pytest

from hexagonal import db, FacultyPatron, app
from hexagonal.auth.permissions import Permission
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal import Librarian, AVMaterial
from hexagonal.model.student_patron import StudentPatron
from hexagonal import User, Loan, Patron, QueuedRequest, Professor
from hexagonal.model.visiting_professor_patron import VisitingProfessorPatron

app.testing = True
client = app.test_client()


def state_of_system():
    d1 = create_instance(Book, title='Introduction to Algorithms',
                         authors=['Thomas H. Cormen', 'Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
                         publisher='MIT Press', publishment_year=2009, edition=3,
                         reference=False, price=5000,
                         keywords=['Algorithms', 'Data Structures', 'Complexity', 'Computational Theory'])

    d2 = create_instance(Book, title='Algorithms + Data Structures = Programs',
                         authors=['Niklaus Wirth'],
                         publisher='Prentice Hall PTR', publishment_year=1978, edition=1,
                         reference=False, price=5000,
                         keywords=['Algorithms', 'Data Structures', 'Search Algorithms', 'Pascal'])

    d3 = create_instance(Book, title='The Art of Computer Programming',
                         authors=['Donald E. Knuth'],
                         publisher='Addison Wesley Longman Publishing Co., Inc.',
                         publishment_year=1997, edition=3, price=5000,
                         keywords=['Algorithms', 'Combinatorial Algorithms', 'Recursion'])

    # copies_d1 = [create_instance(DocumentCopy, document=d1) for i in range(3)]
    # copies_d2 = [create_instance(DocumentCopy, document=d2) for i in range(3)]
    # copies_d3 = [create_instance(DocumentCopy, document=d3) for i in range(2)]

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

    # docs_set = [copies_d1, copies_d2, copies_d3, d1, d2, d3]
    docs_set = [d1, d2, d3]
    users_set_patrons = [p1, p2, p3]
    users_set_students = [s]
    users_set_visiting_profs = [v]

    return docs_set, users_set_patrons, users_set_students, users_set_visiting_profs


def state_of_system_librarians():
    reload_db()
    l1 = register_test_account(Librarian, login='librarian1', password='yolo69')
    l1.access_level = 1
    l2 = register_test_account(Librarian, login='librarian2', password='yolo69')
    l2.access_level = 2
    l3 = register_test_account(Librarian, login='librarian3', password='yolo69')
    l3.access_level = 3

    db.session.add(l1)
    db.session.add(l2)
    db.session.add(l3)
    db.session.commit()

    sys_librarians = Librarian.query

    return sys_librarians


def test_tc2_admin_creates_3_librarians():
    reload_db()
    libr = state_of_system_librarians()
    assert libr.count() == 3


def test_tc3_l1_creates_l1_checks_and_nothing():
    reload_db()
    librs = state_of_system_librarians()
    l1 = librs.filter(Librarian.login == 'librarian1').first()

    assert not l1.has_permission(Permission.create_document)


def test_4_inside():
    librs = state_of_system_librarians()
    l1 = librs.filter(Librarian.login == 'librarian1').first()
    l2 = librs.filter(Librarian.login == 'librarian2').first()
    l3 = librs.filter(Librarian.login == 'librarian3').first()

    if (l2.has_permission(Permission.create_document)):
        d1 = create_instance(Book, title='Introduction to Algorithms',
                             authors=['Thomas H. Cormen', 'Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'],
                             publisher='MIT Press', publishment_year=2009, edition=3,
                             reference=False, price=5000,
                             keywords=['Algorithms', 'Data Structures', 'Complexity', 'Computational Theory'])

        d2 = create_instance(Book, title='Algorithms + Data Structures = Programs',
                             authors=['Niklaus Wirth'],
                             publisher='Prentice Hall PTR', publishment_year=1978, edition=1,
                             reference=False, price=5000,
                             keywords=['Algorithms', 'Data Structures', 'Search Algorithms', 'Pascal'])

        d3 = create_instance(Book, title='The Art of Computer Programming',
                             authors=['Donald E. Knuth'],
                             publisher='Addison Wesley Longman Publishing Co., Inc.',
                             publishment_year=1997, edition=3, price=5000,
                             keywords=['Algorithms', 'Combinatorial Algorithms', 'Recursion'])

        copies_d1 = [create_instance(DocumentCopy, document=d1) for i in range(3)]
        copies_d2 = [create_instance(DocumentCopy, document=d2) for i in range(3)]
        copies_d3 = [create_instance(DocumentCopy, document=d3) for i in range(3)]
        docs_created = True;
    if (l2.has_permission(Permission.create_patron)):
        p1 = register_test_account(Professor, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                                   card_number=1010)
        p2 = register_test_account(Professor, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
                                   card_number=1011)
        p3 = register_test_account(Professor, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
                                   card_number=1100)
        s = register_test_account(StudentPatron, name='Andrey Velo', address=': Avenida Mazatlan 250', phone='30004',
                                  card_number=1101)
        v = register_test_account(VisitingProfessorPatron, name='Veronika Rama', address='Stret Atocha, 27',
                                  phone='30005',
                                  card_number=1110)
        patrons_created = True
        librarians = [l1, l2, l3]
        flags = [docs_created, patrons_created]
        docs_set = [d1, d2, d3, copies_d1, copies_d2, copies_d3]
        users_set_patrons = [p1, p2, p3]
        users_set_students = [s]
        users_set_visiting_profs = [v]
        return librarians, docs_set, users_set_patrons, users_set_students, users_set_visiting_profs, flags


def test_tc4_l2_creates_lots_of_thigns_and_that_works_wow():
    # l2 creates 3 copies of d1, 3 copies of d2, and 3 copies of d3.
    # patrons s, p1, p2, p3 and v.
    # l2 checks inf of system
    reload_db()
    inf = test_4_inside()
    flags = inf[len(inf) - 1]
    docs_created = flags[0]
    patrons_created = flags[1]
    assert docs_created and patrons_created

def test_5_inside():
    inf = test_4_inside()
    l3 = inf[0][2]
    if l3.has_permission(Permission.delete_document):
        docs_set = inf[1]
        db.session.delete(docs_set[0].copies[0])
        db.session.commit()

    return inf[0], docs_set, inf[2], inf[3], inf[4], inf[5]

def test_tc5_l3_works_with_docs():
    reload_db()
    inf = test_5_inside()
    docs = inf[1]
    # assert docs[4] is DocumentCopy
    assert len(docs[0].copies) == 2
