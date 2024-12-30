import os
import pandas as pd
import tabula
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Convert PDF to CSV
        csv_output = os.path.join(app.config['OUTPUT_FOLDER'], file.filename.replace('.pdf', '.csv'))
        try:
            tabula.convert_into(file_path, csv_output, output_format="csv", pages="all")
        except Exception as e:
            return jsonify({"error": f"Failed to convert PDF: {e}"})
        
        # Load CSV for analysis
        try:
            data = pd.read_csv(csv_output)
            # Generate basic analysis
            analysis = {
                "num_rows": len(data),
                "num_columns": len(data.columns),
                "columns": list(data.columns),
                "missing_values": data.isnull().sum().to_dict(),
                "summary": data.describe(include='all').to_dict()
            }
        except Exception as e:
            return jsonify({"error": f"Failed to analyze CSV: {e}"})
        
        return jsonify({
            "message": "File successfully processed",
            "analysis": analysis,
            "csv_download": f"/download/{os.path.basename(csv_output)}"
        })
    else:
        return jsonify({"error": "Unsupported file format. Only PDFs are allowed."})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
