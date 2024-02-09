from flask import Flask, request, jsonify

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
    try:
        #check for file provided
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        csv_file = request.files['file']
        
        #check for content
        if csv_file.filename == '':
            return jsonify({"error": "Empty file provided"}), 400
        
        #check extension
        if not csv_file.filename.endswith('.csv'):
            return jsonify({"error": "Invalid file format: Expected CSV"}), 400
        
        #read content
        csv_data = csv_file.read().decode('utf-8')
        
        #generate list of dictionaries
        csv_rows = []
        for row in csv_data.split('\n'):
            if row.strip():
                values = row.split(',')
                row_dict = {}
                for index, value in enumerate(values):
                    row_dict[f'val{index+1}'] = value.strip()
                csv_rows.append(row_dict)
        
        #validate format
        is_valid, message = csv_validate(csv_rows)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        return jsonify({"message": "CSV file uploaded successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
