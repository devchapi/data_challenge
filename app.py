import os
from flask import Flask, request, jsonify
from src.utils.processing import rename_timestamp, upload_to_database, execute_employees_by_department_job_service, execute_hired_over_mean_service
from src.utils.constants import Constants

app = Flask(__name__)


@app.route('/upload/csv', methods=['POST'])
def upload_csv():
    #check file
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    csv_file = request.files['file']

    #check content
    if csv_file.filename == '':
        return jsonify({"error": "Empty file provided"}), 400

    #check format
    if not csv_file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format: Expected CSV"}), 400

    if not csv_file.filename in ['departments.csv', 'hired_employees.csv', 'jobs.csv']:
        return jsonify({"error": "Invalid file format: Unexpected filename"}), 400

    filename = csv_file.filename

    #temporary location constant
    path = Constants.uploaded_files_path 
    file_timestamp = rename_timestamp(filename)
    path_file =  f"{path}{file_timestamp}"
    csv_file.save(path_file)

    #get entity
    base_name = os.path.basename(filename)
    entity = base_name.split('.')[0]  

    #upload and migrate
    upload_to_database(path_file, entity)

    return jsonify({"message": "CSV file uploaded and processed successfully"}), 200


@app.route('/employees_by_department_job', methods=['GET'])
def employees_by_department_job():
    query = Constants.query_quarters

    data = execute_employees_by_department_job_service(query)

    return jsonify(data)


@app.route('/hired_over_mean', methods=['GET'])
def departments_hiring_most():
    query = Constants.query_more_hired

    data = execute_hired_over_mean_service(query)

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
