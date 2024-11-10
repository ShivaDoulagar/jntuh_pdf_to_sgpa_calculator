from flask import Flask,render_template,request
import conversion 
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)



@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        if request.method == 'GET':
            return render_template("index.html")
        
        elif request.method == 'POST':
            convert = conversion.Conversion()  # Instantiate the Conversion class

            uploaded_file = request.files['file']
            if uploaded_file and uploaded_file.filename.endswith('.pdf'):
                # Secure the filename and save the uploaded PDF
                file_name = secure_filename(uploaded_file.filename)
                pdf_file = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                uploaded_file.save(pdf_file)
                file_name = uploaded_file.filename
                first_part = file_name.split('.')[0]
                csv_file = first_part + ".csv"
                
                # Define the output path for the CSV file
                csv_file_path = os.path.join(app.config['CONVERTED_FOLDER'], csv_file)

                # Convert PDF to CSV
                convert.pdf_to_csv(pdf_file, csv_file_path)

               
                calculated_sgpa = convert.calculate(csv_file_path)

  
                return render_template('result.html', result = calculated_sgpa )

            else:
                return "Invalid file format. Please upload a PDF."
    
    except Exception:
        return "Some error occurred! Please try again."




if __name__ == '__main__':
    app.run(debug=True)