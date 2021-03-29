from setuptools import setup, find_packages

import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='cookielog',
    description='Simple command-line application to find the most frequent cookie',
    version='0.0.1',
    package=find_packages(),
    install_requires=[
        'Click'
    ],
    python_requires='>=3.6',
    py_modules=['cookielog'],
    entry_points='''
        [console_scripts]
        cookielog=cookielog:cli
    ''',
    author='Hossein Fakhari',
    keyword='cookie, log, search, csv',
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    author_email='fakhari.hossein@gmail.com',
    url='https://github.com/hosseinfakhari/cookielog',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ]
)
