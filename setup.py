from setuptools import setup

setup(
    name='yacmt_gui',
    version='0.3',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    license='MIT',
    packages=['yacmt_gui'],
    install_requires=['yacmt', 'PyQt5', 'psycopg2', 'sqlalchemy'],
    extras_require={'dev': ['flake8']},
    entry_points={'console_scripts': ['yacmt_gui = yacmt_gui.main:main']})
