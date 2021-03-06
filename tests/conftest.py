# pylint: disable=redefined-outer-name

# Standard library imports
from datetime import date, timedelta

# Third party imports
import pytest

# Local application imports
from backend.derivatex_models import Derivative, User, ReportHead, Action, ActionType
from backend.app import Application
from backend.db import db


@pytest.fixture(scope='session', autouse=True)
def test_app():
    # Initialise test app instance
    app = Application.getTestApp()

    # Ensure app is configured for Testing
    if not app.config['TESTING']:
        raise SystemExit('App must be conifgured for testing')

    # Return the flask app
    return app


@pytest.fixture(scope='session', autouse=True)
def test_client(test_app):
    # Get test client
    testing_client = test_app.test_client()

    # Establish an application context before running the tests.
    ctx = test_app.app_context()
    ctx.push()

    # Return the test client
    yield testing_client

    ctx.pop()


@pytest.fixture(autouse=True)
def clean_database():
    # Clean the session and all tables in the test database
    db.session.rollback()
    db.drop_all(bind=None)
    db.create_all(bind=None)


@pytest.fixture
def free_derivtive_id():
    # Return an invalid id
    return -1


@pytest.fixture
def free_user_id():
    # Return an invalid id
    return -1


@pytest.fixture
def free_report_id():
    # Return an invalid id
    return -1


@pytest.fixture
def dummy_derivative():
    today = date.today()

    return Derivative(
        code='doe',
        buying_party='foo',
        selling_party='bar',
        asset='Stocks',
        quantity=1,
        strike_price=20.20,
        notional_curr_code='USD',
        date_of_trade=today,
        maturity_date=today + timedelta(days=365)
    )


# TODO: revisit
@pytest.fixture
def dummy_derivative_json(dummy_derivative):
    return {
        'code': dummy_derivative.code,
        'buying_party': dummy_derivative.buying_party,
        'selling_party': dummy_derivative.selling_party,
        'asset': dummy_derivative.asset,
        'quantity': dummy_derivative.quantity,
        'strike_price': dummy_derivative.strike_price,
        'notional_curr_code': dummy_derivative.notional_curr_code,
        'maturity_date': str(dummy_derivative.maturity_date),
        'date_of_trade': str(dummy_derivative.date_of_trade)
    }


@pytest.fixture
def dummy_abs_derivative(dummy_derivative):
    # Get the current date
    today = date.today()
    # Modify the dummy derivatives date of trade to make it absolute
    dummy_derivative.date_of_trade = today - timedelta(days=365)
    # Return absolute dummy derivative
    return dummy_derivative


@pytest.fixture
def dummy_user():
    return User(
        f_name='f_name',
        l_name='l_name',
        email='email',
        password='password'
    )


@pytest.fixture
def dummy_user_2():
    return User(
        f_name='f_name2',
        l_name='l_name2',
        email='email2',
        password='password123'
    )


@pytest.fixture
def dummy_updates():
    return {
        'buying_party': 'newfoo',
        'selling_party': 'newbar',
        'asset': 'newbaz'
    }


@pytest.fixture
def dummy_action():
    return Action(
        type=ActionType.ADD,
        timestamp=date.today(),
        update_log=None,
    )


@pytest.fixture
def dummy_report_head():
    return ReportHead(
        target_date=date.today(),
        creation_date=date.today(),
        version=1,
        derivative_count=0,
    )
