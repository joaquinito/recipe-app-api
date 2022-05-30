'''
Test custom Django management commands.
'''
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patch will mock the behaviour of the command 'check', which allows you to
# check the status of the db
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    '''Test commands.'''

    # patched_check is a mock object passed as an argument, and we use it to
    # customize the behaviour
    def test_wait_for_db_ready(self, patched_check):
        '''Test waiting for database if database ready.'''
        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # We mock the sleep function so that the tests are not slowed down (the
    # mock will not actually sleep)
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        '''Test waiting for database when getting OperationalError'''
        # Side effect allows you to parse in various different items that get
        # handled differently depending on their type. If we parse in an
        # exception, then the mocking library knows that it should raise that
        # exception. Here we say that the first two times we call the mocked
        # method, we want it to raise the Psycopg2Error, then the next three
        # time it'll raise the OperationalError, and finally it return True.
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
