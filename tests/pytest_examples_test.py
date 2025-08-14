from examples.pytest_examples import add, multiply, subtract, BankAccount, InsufficientFunds
import pytest

def test_add():
    assert add(1, 2) == 3
    assert add(2, 3) == 5

def test_multiply():
    assert multiply(1, 2) == 2
    assert multiply(2, 3) == 6
    assert multiply(3, 5) == 15


# add a test with parameters
# will show the test ran multiple times
''' Example:
tests/pytest_examples_test.py::test_subtract[1-2--1] PASSED                                                                                                                                             [ 50%]
tests/pytest_examples_test.py::test_subtract[3-2-1] PASSED                                                                                                                                              [ 66%]
tests/pytest_examples_test.py::test_subtract[10-5-5] PASSED                                                                                                                                             [ 83%]
tests/pytest_examples_test.py::test_subtract[5-5-0] PASSED 
'''
@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, -1),
    (3, 2, 1),
    (10, 5, 5),
    (5, 5, 0),
])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected


# testing a class
def test_bank_withdrawal():
    bank = BankAccount(starting_balance=50)
    bank.withdraw(20)
    assert bank.balance == 30

def test_bank_deposit():
    bank = BankAccount(starting_balance=50)
    bank.deposit(10)
    assert bank.balance == 60

def test_bank_interest():
    bank = BankAccount(starting_balance=50)
    bank.collect_interest()
    # was failing with a value of like 55.00000000001
    assert round(bank.balance,2) == 55

# fixtures
# run a function before running a test
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(starting_balance=50)


# use fixture to reduce code duplication
def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_set_initial(bank_account):
    assert bank_account.balance == 50

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(20)
    zero_bank_account.withdraw(10)
    assert zero_bank_account.balance == 10


@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (10,5,5),
    (100,0,100)
])
def test_multiple_transactions(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(zero_bank_account):
    # handle an exception being raised
    # test will fail if exception isn't raised
    with pytest.raises(InsufficientFunds):
        zero_bank_account.deposit(10)
        zero_bank_account.withdraw(20)


