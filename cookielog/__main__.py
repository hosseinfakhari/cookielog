import os
import re
import sys
from datetime import datetime

import click


def validate_date(date: str):
    if not bool(re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', date)) \
            or len(date) != 10:
        raise RuntimeError("Invalid format! Use %y-%m-%d. e.g: 2021-03-28")


def validate_file(file_path: str):
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
                print(cookie)


@click.command()
@click.option('-f', '--file', required=True, help='input file name', type=str)
@click.option('-d', '--date', required=True, help='target date e.g 2017-09-09')
def cli(file, date):
    try:
        validate_date(date)
        validate_file(file)
    except RuntimeError as error:
        print(f'Runtime Error: {error}')
        sys.exit(0)
    search_date = datetime.strptime(date, '%Y-%m-%d')
    date_cookies = get_date_cookies(file, search_date)
    find_most_active_cookie(date_cookies)


if __name__ == '__main__':
    cli()
