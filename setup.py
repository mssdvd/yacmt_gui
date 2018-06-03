from setuptools import setup

setup(
    name='yacmt_gui',
    version='0.2.3',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacmt_gui'],
    install_requires=[
        'yacmt', 'PyQt5', 'requests', 'psycopg2', 'psycopg2-binary',
        'sqlalchemy'
    ],
    extras_require={'dev': ['flake8']},
    entry_points={'console_scripts': ['yacmt_gui = yacmt_gui.main:main']})
