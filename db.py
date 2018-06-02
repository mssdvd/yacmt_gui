import datetime
import json
from os.path import expanduser
from typing import Any, Dict

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # type: Any
sqlite_db = "sqlite:///{}/yacmt.db".format(expanduser("~"))
psgsql_db = "***REMOVED***"

sqlite_engine = create_engine(sqlite_db)


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    description = Column(String(100))

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    vehicle = Column(ForeignKey('vehicles.id'), nullable=False)
    datetime = Column(DateTime, nullable=False)
    sent = Column(Boolean)
    eng_load = Column(Integer)
    eng_cool_temp = Column(Integer)
    intake_manifold_abs_press = Column(Integer)
    eng_rpm = Column(Integer)
    speed = Column(Integer)
    intake_air_temp = Column(Integer)
    mass_air_flow = Column(Integer)
    throttle_pos = Column(Integer)
    run_time = Column(Integer)
    control_mod_voltage = Column(Integer)


def init_db():
    """Create a SQLite database if it doesn't exits"""
    Base.metadata.create_all(sqlite_engine)
    Session = sessionmaker(bind=sqlite_engine)
    session = Session()
    if session.query(Vehicle.id).scalar() is None:
        # add a default vehicle
        session.add(Vehicle("Toyota Yaris", "Fantastica auto"))
        session.commit()


def insert_vehicle(name: str, description: str):
    """Insert a new vehicle"""
    new_vehicle = Vehicle(name, description)
    Session = sessionmaker(bind=sqlite_engine)
    session = Session()
    session.add(new_vehicle)
    session.commit()


def insert_report(data: Dict, vehicle: int = 1):
    """Insert a new report"""
    data.update({
        "vehicle": vehicle,
        "datetime": datetime.datetime.now(),
        "sent": False
    })
    session = sessionmaker(bind=sqlite_engine)
    session = session()
    new_report = Report(**data)
    session.add(new_report)
    session.commit()
