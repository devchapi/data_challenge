import os
import json 
from datetime import datetime
import dateutil.parser
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from src.models.hired_employees_model import Employee
from src.models.departments_model import Department
from src.models.jobs_model import Job

def safe_int(value):
    return int(value) if value is not None else None

def safe_date(value):
    return dateutil.parser.parse(value) if value is not None else None

def csv_validate(data):
    try:
        for entry in data:
            if not int(entry['val1']):
                return False, "Invalid data format: field_1 not a integer"
    except KeyError as e:
        return False, f"Invalid data format"
    return True, "CSV data format is valid"

def upload_to_database(filename, entity):
    with open('src/utils/config.json', 'r') as f:
        config = json.load(f)
    
    connection_cad = f"mysql+mysqldb://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/{config['mysql']['database']}"
    
    engine = create_engine(connection_cad)

    Session = sessionmaker(bind=engine)
    session = Session()

    if entity == 'hired_employees':
        Employee.metadata.create_all(engine)
    elif entity == 'departments':
        Department.metadata.create_all(engine)
    elif entity == 'jobs':
        Job.metadata.create_all(engine)
    else: 
        return 'ERROR CREATING TABLE'

    #batch_size = 1000
    with open(filename, 'r') as file:
        lines = file.readlines()
        batch = []
        for line in lines:
            data = line.strip().split(',')
            for i, value in enumerate(data):
                if value == '':
                    data[i] = None
            if entity == 'hired_employees':
                hire_date = safe_date(data[2])
                record = Employee(id=safe_int(data[0]) , name=data[1], hire_date=hire_date, department_id=safe_int(data[3]), job_id=safe_int(data[4]))
            elif entity == 'departments':
                record = Department(id=safe_int(data[0]) , department=data[1])
            elif entity == 'jobs':
                record = Job(id=safe_int(data[0]) , job=data[1])

            batch.append(record)

            try:
                session.merge(record)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                print(f"Error inserting record: {e}")

    session.close()

def rename_timestamp(filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{timestamp}{ext}"

    return new_filename

def execute_employees_by_department_job_service(query):
    with open('src/utils/config.json', 'r') as f:
        config = json.load(f)
    
    connection_cad = f"mysql+mysqldb://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/{config['mysql']['database']}"
    
    engine = create_engine(connection_cad)

    try:
        results = engine.execute(query)
        
        employee_data = []
        for row in results:
            department = row[0]
            job = row[1]
            quarters = {'Q1': str(row[2]), 'Q2': str(row[3]), 'Q3': str(row[4]), 'Q4': str(row[5])}
            employee_data.append({'department': department, 'job': job, 'quarters': quarters})
        
        return employee_data

    except Exception as e:
        return f"Error executing service: {e}"

def execute_hired_over_mean_service(query):
    with open('src/utils/config.json', 'r') as f:
        config = json.load(f)
    
    connection_cad = f"mysql+mysqldb://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/{config['mysql']['database']}"
    
    engine = create_engine(connection_cad)

    try:
        results = engine.execute(query)
        
        result_data = []
        for row in results:
            department_id = str(row[0])
            department_name = row[1]
            employees_hired = str(row[2])
            result_data.append({'id': department_id, 'department': department_name, 'hired': employees_hired})
        
        return result_data

    except Exception as e:
        return f"Error executing service: {e}"


