import pytest
from tests.jsonrpc import call


def test_something():
    call('auth.login', ['asdf', 'ghj'])
