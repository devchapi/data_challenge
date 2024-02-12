from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'hired_employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    hire_date = Column(DateTime)
    department_id = Column(Integer)
    job_id = Column(Integer)
