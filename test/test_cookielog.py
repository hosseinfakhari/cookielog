import contextlib
import io
import os
from datetime import datetime
from unittest import TestCase
from cookielog import (
    validate_date,
    find_most_active_cookie,
    validate_file,
    get_date_cookies
)


class TestCookieLog(TestCase):
    def setUp(self) -> None:
        self.cookie_filename = 'data/cookies.csv'
        self.tmp_file = 'tmp.csv'
        with open(self.tmp_file, 'w') as tmp_file:
            tmp_file.write('some data')
            tmp_file.close()

    def tearDown(self) -> None:
        os.remove(self.tmp_file)

    def test_invalid_date_length(self):
        wrong_date = '17-01-08'
        with self.assertRaises(ValueError):
            validate_date(wrong_date)

    def test_invalid_date_values(self):
        wrong_date = '2017-01-80'
        with self.assertRaises(ValueError):
            validate_date(wrong_date)

    def test_valid_date(self):
        correct_date = '2017-01-01'
        f = validate_date(correct_date)
        self.assertEqual(f, None)

    def test_file_not_exists(self):
        file_path = 'some_random_name'
        with self.assertRaises(RuntimeError):
            validate_file(file_path)

    def test_pass_directory_instead_of_file(self):
        file_path = '/home'
        with self.assertRaises(RuntimeError):
            validate_file(file_path)

    def test_invalid_file_format(self):
        with self.assertRaises(RuntimeError):
            validate_file(self.tmp_file)

    def test_correct_file(self):
        f = validate_file(self.cookie_filename)
        self.assertEqual(f, None)

    def test_get_existing_date_cookies(self):
        target_date = datetime.strptime('2018-06-01', '%Y-%m-%d')
        cookies = get_date_cookies(self.cookie_filename, target_date)
        self.assertEqual(len(cookies), 52)

    def test_get_none_existing_date_cookies(self):
        target_date = datetime.strptime('2020-06-01', '%Y-%m-%d')
        cookies = get_date_cookies(self.cookie_filename, target_date)
        self.assertEqual(len(cookies), 0)

    def test_find_most_active_cookie(self):
        target_date = datetime.strptime('2018-06-01', '%Y-%m-%d')
        cookies = get_date_cookies(self.cookie_filename, target_date)
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            find_most_active_cookie(cookies)
        self.assertTrue('AzWXSm21KK6zT5yS' in f.getvalue())
