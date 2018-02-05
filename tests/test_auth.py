import pytest
from tests.jsonrpc import call
from hexagonal.auth import decode_token


def root_login():
    return call('auth.login', ['root', 'toor'])


def get_login_pair():
    get_login_pair.cnt += 1
    return (
        'testLogin_{}'.format(get_login_pair.cnt),
        'testPassword_{}'.format(get_login_pair.cnt)
    )


get_login_pair.cnt = 0


# decode_token raises an exception when unable to parse


def test__root_login__should_not_fail():
    decode_token(root_login())


def test__registering_from_root__should_not_fail():
    token = root_login()
    login, password = get_login_pair()
    call('auth.register', {
        'login': login,
        'password': password,
        'role': 'student-patron',
        'address': '123',
        'name': 'One Two',
        'card_number': 123,
        'phone': 123
    }, token)


def test__just_registered_user__should_be_able_to_login():
    token = root_login()
    login, password = get_login_pair()
    call('auth.register', {
        'login': login,
        'password': password,
        'role': 'student-patron',
        'address': '123',
        'name': 'One Two',
        'card_number': 123,
        'phone': 123
    }, token)
    decode_token(call('auth.login', {
        'login': login,
        'password': password
    }))

#ToDo
#def test__creating_new_document_book_is_correct():

#def test__creating_new_document_journal_is_correct():

#def test_creating_new_document_av_file_is_correct():

#def access_of_librariant_to_adding_new_book_to_system_is_correct():

#def access_of_student_to_booking_system_is_correct():

#def access_of_TA_to_booking_system_is_correct():
