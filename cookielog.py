"""
cookielog find the most active cookie in a csv log file.
"""
import os
import re
import sys
from datetime import datetime

import click


def validate_date(date: str):
    """
    Validates date string with regexp and datetime library parser
    """
    if not bool(re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', date)) \
            or len(date) != 10:
        raise ValueError("Invalid format! Use %y-%m-%d. e.g: 2021-03-28")
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError as error:
        raise error


def validate_file(file_path: str):
    """
    Validates input file
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path) as file:
            csv_headers = file.readline()
            if ['cookie', 'timestamp\n'] != csv_headers.split(','):
                raise RuntimeError('input file format is not valid')
            datetime_format = file.readline().split(',')[1]
            match = bool(re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]'
                                  r'{2}:[0-9]{2}\+[0-9]{2}:[0-9]{2}',
                                  datetime_format))
            if len(datetime_format) != 26 or not match:
                raise RuntimeError('input file format is not valid')
    else:
        raise RuntimeError(f'No Such a file: {file_path}')


def get_date_cookies(filename: str, target_date: datetime):
    """
    Scan csv file and returns list of cookies in specific date
    """
    cookies = []
    with open(filename) as file:
        file.readline()
        for row in file:
            r_cookie, r_date = row.split(',')
            rd = datetime.strptime(r_date.rstrip('\n'), '%Y-%m-%dT%H:%M:%S%z')
            if rd.date() == target_date.date():
                cookies.append(r_cookie)
    return cookies


def find_most_active_cookie(cookies):
    """
    Find and print most active cookie by calculating its frequency
    """
    if len(cookies) > 0:
        freq = {}
        for cookie in cookies:
            if cookie in freq:
                freq[cookie] += 1
            else:
                freq[cookie] = 1
        most = max(freq.values())
        for cookie, frequency in freq.items():
            if frequency == most:
                sys.stdout.write(f'{cookie}\n')


@click.command()
@click.option('-f', '--file', required=True, help='input file name', type=str)
@click.option('-d', '--date', required=True, help='target date e.g 2017-09-09')
def cli(file, date):
    """
    parsing commandline argument for input file and target date
    """
    try:
        validate_date(date)
        validate_file(file)
    except RuntimeError as error:
        sys.stderr.write(f'Runtime Error: {error}\n')
        sys.exit(0)
    except ValueError as error:
        sys.stderr.write(f'Value Error: {error}\n')
        sys.exit(0)
    search_date = datetime.strptime(date, '%Y-%m-%d')
    date_cookies = get_date_cookies(file, search_date)
    find_most_active_cookie(date_cookies)


if __name__ == '__main__':
    cli()
