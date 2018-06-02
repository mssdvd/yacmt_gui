from setuptools import setup

setup(
    name='yacmt_gui',
    version='0.1',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacmt_gui'],
    install_requires=['pyqt5', 'requests', 'psycopg2', 'sqlalchemy'],
    extras_require={'dev': ['flake8']},
    entry_points={'console_scripts': ['yacmt_gui = main:main']})
