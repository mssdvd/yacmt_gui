from setuptools import setup

setup(
    name='yacmt_gui',
    version='0.4',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacmt_gui'],
    install_requires=['yacmt_core', 'PyQt5', 'psycopg2', 'sqlalchemy'],
    extras_require={'dev': ['flake8']},
    entry_points={'console_scripts': ['yacmt_gui = yacmt_gui.main:main']},
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ])
