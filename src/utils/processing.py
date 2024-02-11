import os
import json 
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from src.models.hired_employees_model import Employee
from src.models.departments_model import Department
from src.models.jobs_model import Job

def upload_to_database(filename, entity):
    with open('src/utils/config.json', 'r') as f:
        config = json.load(f)
    
    connection_cad = f"mysql+mysqldb://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/{config['mysql']['database']}"
    
    print(connection_cad)
    engine = create_engine(connection_cad)

    Session = sessionmaker(bind=engine)
    session = Session()

    if entity == 'employees':
        Employee.metadata.create_all(engine)
    elif entity == 'departments':
        Department.metadata.create_all(engine)
    elif entity == 'jobs':
        Job.metadata.create_all(engine)

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(',')
            if entity == 'employees':
                hire_date = datetime.fromisoformat(data[2])
                record = Employee(name=data[1], hire_date=hire_date, department_id=int(data[3]), job_id=int(data[4]))
            elif entity == 'departments':
                record = Department(department=data[1])
            elif entity == 'jobs':
                record = Job(job=data[1])

            try:
                session.add(record)
                session.commit()
            except IntegrityError as e:
                session.rollback()  # Rollback the transaction if an IntegrityError occurs
                print(f"Error inserting record: {e}")

    session.close()

def rename_timestamp(filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{timestamp}{ext}"

    return new_filename
