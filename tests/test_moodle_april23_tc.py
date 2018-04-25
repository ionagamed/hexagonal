from freezegun import freeze_time
import datetime

import pytest

from hexagonal import db, FacultyPatron, app, Document, Admin
from hexagonal.auth.permissions import Permission
from tests.common import call, root_login, register_test_account, create_instance, reload_db
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal import Librarian, AVMaterial
from hexagonal.model.student_patron import StudentPatron
from hexagonal import User, Loan, Patron, QueuedRequest, Professor
from hexagonal.model.visiting_professor_patron import VisitingProfessorPatron
from hexagonal.model.log_entry import log, LogEntry

app.testing = True
client = app.test_client()


def create_admin():
    if Admin.query.count() > 0:
        raise ValueError


def state_of_system_librarians():
    reload_db()
    l1 = register_test_account(Librarian, login='librarian1', password='yolo69') l1.access_level = 1 log('admin', 'created', 'librarian1')
    l2 = register_test_account(Librarian, login='librarian2', password='yolo69')
    l2.access_level = 2
    log('admin', 'created', 'librarian2')
    l3 = register_test_account(Librarian, login='librarian3', password='yolo69')
    l3.access_level = 3
    log('admin', 'created', 'librarian3')

    db.session.add(l1)
    db.session.add(l2)
    db.session.add(l3)
    db.session.commit()

    sys_librarians = Librarian.query

    return sys_librarians


def test_tc1_only_one_admin():
    with pytest.raises(ValueError):
        create_admin()


def test_tc2_admin_creates_3_librarians():
    reload_db()
    libr = state_of_system_librarians()
    assert libr.count() == 3


def test_tc3_l1_creates_l1_checks_and_nothing():
    reload_db()
    librs = state_of_system_librarians()
    l1 = librs.filter(Librarian.login == 'librarian1').first()

    assert not l1.has_permission(Permission.create_document)


def tc4_inside():
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
        log('l2', 'created', 'd1')
        d2 = create_instance(Book, title='Algorithms + Data Structures = Programs',
                             authors=['Niklaus Wirth'],
                             publisher='Prentice Hall PTR', publishment_year=1978, edition=1,
                             reference=False, price=5000,
                             keywords=['Algorithms', 'Data Structures', 'Search Algorithms', 'Pascal'])
        log('l2', 'created', 'd2')
        d3 = create_instance(Book, title='The Art of Computer Programming',
                             authors=['Donald E. Knuth'],
                             publisher='Addison Wesley Longman Publishing Co., Inc.',
                             publishment_year=1997, edition=3, price=5000,
                             keywords=['Algorithms', 'Combinatorial Algorithms', 'Recursion'])
        log('l2', 'created', 'd3')
        copies_d1 = [create_instance(DocumentCopy, document=d1) for i in range(3)]
        log('l2', 'created', '3 copy d1')
        copies_d2 = [create_instance(DocumentCopy, document=d2) for i in range(3)]
        log('l2', 'created', '3 copy d2')
        copies_d3 = [create_instance(DocumentCopy, document=d3) for i in range(3)]
        log('l2', 'created', '3 copy d3')
        docs_created = True
    if (l2.has_permission(Permission.create_patron)):
        p1 = register_test_account(Professor, name='Sergey Afonso', address='Via Margutta, 3', phone='30001',
                                   card_number=1010)
        log('l2', 'created', 'p1')
        p2 = register_test_account(Professor, name='Nadia Teixeira', address='Via Sacra, 13', phone='30002',
                                   card_number=1011)
        log('l2', 'created', 'p2')
        p3 = register_test_account(Professor, name='Elvira Espindola', address='Via del Corso, 22', phone='30003',
                                   card_number=1100)
        log('l2', 'created', 'p3')
        s = register_test_account(StudentPatron, name='Andrey Velo', address=': Avenida Mazatlan 250', phone='30004',
                                  card_number=1101)
        log('l2', 'created', 's')
        v = register_test_account(VisitingProfessorPatron, name='Veronika Rama', address='Stret Atocha, 27',
                                  phone='30005',
                                  card_number=1110)
        log('l2', 'created', 'v')
        patrons_created = True

    librarians = [l1, l2, l3]
    flags = [docs_created, patrons_created]
    docs_set = [d1, d2, d3, copies_d1, copies_d2, copies_d3]
    users_set_patrons = [p1, p2, p3]
    users_set_students = [s]
    users_set_visiting_profs = [v]
    return librarians, docs_set, users_set_patrons, users_set_students, users_set_visiting_profs, flags


def test_tc4_l2_creates_lots_of_thigns_and_that_works_wow():
    reload_db()
    inf = tc4_inside()
    flags = inf[len(inf) - 1]
    docs_created = flags[0]
    patrons_created = flags[1]
    assert docs_created and patrons_created


def tc5_inside():
    inf = tc4_inside()
    l3 = inf[0][2]
    if l3.has_permission(Permission.delete_document):
        docs_set = inf[1]
        log('l3', 'deleted', '1 copy d1')
        db.session.delete(docs_set[0].copies[0])
        db.session.commit()

    return inf[0], docs_set, inf[2], inf[3], inf[4], inf[5]


def test_tc5_l3_works_with_docs():
    reload_db()
    inf = tc5_inside()
    docs = inf[1]
    l2 = inf[0][1]
    assert len(docs[0].copies) == 2


def tc6_inside():
    inf = tc4_inside()
    l1 = inf[0][0]
    p1 = inf[2][0]
    p2 = inf[2][1]
    p3 = inf[2][2]
    s = inf[3][0]
    v = inf[4][0]
    d3 = inf[1][2]
    copies_d3 = inf[1][5]
    loan_p1_d3 = p1.checkout(copies_d3[0])
    loan_p1_d3.status = Loan.Status.approved
    log('p1', 'checkouted', '1 copy d3')
    loan_p2_d3 = p2.checkout(copies_d3[1])
    loan_p2_d3.status = Loan.Status.approved
    log('p2', 'checkouted', '1 copy d3')
    loan_s_d3 = s.checkout(copies_d3[2])
    loan_s_d3.status = Loan.Status.approved
    log('s', 'checkouted', '1 copy d3')
    loans = [loan_p1_d3, loan_p2_d3, loan_s_d3]

    qr_v_d3 = QueuedRequest(
        patron=v,
        document=d3)
    log('v','checkout','1 copy d3')
    db.session.add(qr_v_d3)
    qr_p3_d3 = QueuedRequest(
        patron=p3,
        document=d3
    )
    log('p3', 'checkout','1 copy d3')
    db.session.add(qr_p3_d3)

    flag_l1_no_out_req = False

    db.session.commit()

    response = client.post('/login', data={
        'login': 'librarian1',
        'password': 'yolo69'
    })

    db.session.commit()

    response = client.get('/admin/documents/3/outstanding_request')
    if response.status == '302 FOUND' and response.location == 'http://localhost/login':
        flag_l1_no_out_req = True

    # if not l1.has_permission(Permission.outstanding_request):
    #     flag_l1_no_out_req = True
    #     log('l1','outst req','d3')
    # if not flag_l1_no_out_req:
    #     log('l1', 'fail outst req', 'd3')

    return inf[0], inf[1], loans, inf[3], inf[4], inf[5], flag_l1_no_out_req


def test_tc6_p1_p2_p3_s_v_has_no_permission_to_checkout_and_l1_cant_place_outstanding_request():
    reload_db()
    inf = tc6_inside()
    flags = inf[6]
    assert flags

def tc7_inside():
    inf = tc4_inside()
    l3 = inf[0][2]
    p1 = inf[2][0]
    p2 = inf[2][1]
    p3 = inf[2][2]
    s = inf[3][0]
    v = inf[4][0]
    copies_d3 = inf[1][5]
    d3 = inf[1][2]
    loan_p1_d3 = p1.checkout(copies_d3[0])
    loan_p1_d3.status = Loan.Status.approved
    db.session.add(loan_p1_d3)
    log('p1', 'checkouted', '1 copy d3')
    loan_p2_d3 = p2.checkout(copies_d3[1])
    loan_p2_d3.status = Loan.Status.approved
    db.session.add(loan_p2_d3)
    log('p2', 'checkouted', '1 copy d3')
    loan_s_d3 = s.checkout(copies_d3[2])
    loan_s_d3.status = Loan.Status.approved
    db.session.add(loan_p2_d3)
    log('s', 'checkouted', '1 copy d3')

    qr_v_d3 = QueuedRequest(
        patron=v,
        document=d3)
    log('v', 'checkout', '1 copy d3')
    db.session.add(qr_v_d3)
    qr_p3_d3 = QueuedRequest(
        patron=p3,
        document=d3
    )
    log('p3', 'checkout', '1 copy d3')
    db.session.add(qr_p3_d3)
    db.session.commit()

    if (l3.has_permission(Permission.outstanding_request)):
        log('l3','outst req','d3')
        d3.outstanding_request()

    waiting_list = QueuedRequest.query.order_by(QueuedRequest.created_at).all()
    waiting_list = sorted(waiting_list, key=lambda x: (x.priority, x.created_at))

    if waiting_list == []:
        flag_waiting_list_empty = True

    if v.queued_documents == [] and p3.queued_documents == []:
        flag_v_and_p3_no_docs = True
    loans = []
    flags = flag_waiting_list_empty and flag_v_and_p3_no_docs
    return inf[0], inf[1], loans, inf[3], inf[4], inf[5], flags


def test_tc7_checkout_outstanding_request_and_sys_is_empty_changes():
    reload_db()
    inf = tc7_inside()
    assert inf[6]

def test_tc8_log_check_after_tc6():
    tc6_inside()
    actual_entries = LogEntry.query.all()
    output = [
        'admin created librarian1',
        'admin created librarian2',
        'admin created librarian3',
        'l2 created d1',
        'l2 created d2',
        'l2 created d3',
        'l2 created 3 copy d1',
        'l2 created 3 copy d2',
        'l2 created 3 copy d3',
        'l2 created p1',
        'l2 created p2',
        'l2 created p3',
        'l2 created s',
        'l2 created v',
        'p1 checkouted 1 copy d3',
        'p2 checkouted 1 copy d3',
        's checkouted 1 copy d3',
        'v checkout 1 copy d3',
        'p3 checkout 1 copy d3'
    ]

    actual_output = []
    for i in actual_entries:
        actual_output.append(' '.join([i.who, i.what, i.obj]))

    assert output == actual_output


def test_tc9_log_check_after_tc7():
    tc7_inside()
    actual_entries = LogEntry.query.all()
    output = [
        'admin created librarian1',
        'admin created librarian2',
        'admin created librarian3',
        'l2 created d1',
        'l2 created d2',
        'l2 created d3',
        'l2 created 3 copy d1',
        'l2 created 3 copy d2',
        'l2 created 3 copy d3',
        'l2 created p1',
        'l2 created p2',
        'l2 created p3',
        'l2 created s',
        'l2 created v',
        'p1 checkouted 1 copy d3',
        'p2 checkouted 1 copy d3',
        's checkouted 1 copy d3',
        'v checkout 1 copy d3',
        'p3 checkout 1 copy d3',
        'l3 outst req d3'
    ]

    actual_output = []
    for i in actual_entries:
        actual_output.append(' '.join([i.who, i.what, i.obj]))

    assert output == actual_output



def test_tc10_search_for_a_book_by_full_title():
    reload_db()
    state = tc4_inside()
    doc = Document._search_in_fields("Introduction to Algorithms", ['title'])
    assert doc is not None


def test_tc11_search_for_a_book_by_title_word():
    reload_db()
    state = tc4_inside()
    search_results = Document._search_in_fields("Algorithms", ['title'])
    assert ['Thomas H. Cormen', 'Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'] == search_results[0].authors
    assert ['Niklaus Wirth'] == search_results[1].authors


def test_tc12_search_for_books_with_keywords():
    reload_db()
    state = tc4_inside()
    search_results = Document._search_in_fields('Algorithms', array_fields=['keywords'])
    assert ['Thomas H. Cormen', 'Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein'] == search_results[0].authors
    assert ["Niklaus Wirth"] == search_results[1].authors
    assert ['Donald E. Knuth'] == search_results[2].authors


def test_tc13_patron_searchs_by_keywords_AND():
    reload_db()
    state = tc4_inside()
    first_clause = Document._search_in_fields_query('Algorithms', array_fields=['keywords'])
    results = Document._search_in_fields_query('Programming', array_fields=['keywords'], apply_to_query=first_clause).all()
    assert results == []


def test_tc14_patron_searchs_by_keywords_OR():
    reload_db()
    state = tc4_inside()
    first_clause = Document._search_in_fields_query('Algorithms', array_fields=['keywords'])
    second_clause = Document._search_in_fields_query("Programming", array_fields=['keywords'])

    results = first_clause.union(second_clause).all()

    assert results[0].authors == ['Thomas H. Cormen', 'Charles E. Leiserson', 'Ronald L. Rivest', 'Clifford Stein']
    assert results[1].authors == ["Niklaus Wirth"]
    assert results[2].authors == ['Donald E. Knuth']


