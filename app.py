import os
from flask import Flask, request, jsonify
from src.utils.processing import rename_timestamp, upload_to_database

app = Flask(__name__)

#Function to validate the content of the data uploaded
def csv_validate(data):
    try:
        for entry in data:
            if not int(entry['val1']):
                return False, "Invalid data format: field_1 not a integer"
    except KeyError as e:
        return False, f"Invalid data format"
    return True, "CSV data format is valid"


@app.route('/upload/csv', methods=['POST'])
def upload_csv():
    # Check if a file is present in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # Get the file from the request
    csv_file = request.files['file']

    # Check if file is empty
    if csv_file.filename == '':
        return jsonify({"error": "Empty file provided"}), 400

    # Check if file extension is CSV
    if not csv_file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format: Expected CSV"}), 400

    if not csv_file.filename in ['departments.csv', 'hired_employees.csv', 'jobs.csv']:
        return jsonify({"error": "Invalid file format: Unexpected filename"}), 400

    filename = csv_file.filename

    # Save the file to a temporary location
    path = "data/input/"
    file_timestamp = rename_timestamp(filename)
    path_file =  f"{path}{file_timestamp}"
    csv_file.save(path_file)

    # Determine the entity based on the filename
    base_name = os.path.basename(filename)
    entity = base_name.split('.')[0]  

    # Upload the file data to the database
    upload_to_database(path_file, entity)

    # Delete the temporary file
    #os.remove(filename)

    return jsonify({"message": "CSV file uploaded and processed successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
