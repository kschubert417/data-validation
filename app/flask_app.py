from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd

app = Flask(__name__)

# Folder where uploaded files will be stored
# YASH NOTE: HERE IS WHERE I HAD TO CHANGE THE FILE PATH FOR UPLOADS FOLDER
# IF YOU RUN INTO ISSUES JUST CHANGE IT BACK TO YOUR FOLDER
# UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'templates', 'ChatGPT', 'test', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TABLE_CONFIG'] = {'masterfile':['item', 'description', 'ítem_type', 'prodfma']}

print(app.config['UPLOAD_FOLDER'])

def get_column_names(csv_file):
    df = pd.read_csv(csv_file)
    return df.columns.tolist()


@app.route('/')
def index():
    print(app.config)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("file[]")
    for file in uploaded_files:
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
    return redirect(url_for('manage'))

@app.route('/manage')
def manage():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('manage.html', files=files)

@app.route('/forms')
def forms():
    file_name = request.args.get('file', default=None)  # Get file name from query parameter
    print(file_name)
    table_name = request.args.get('table', default=None)
    print(f'TABLE NAME: {table_name}')
    if file_name:
        pathcsv = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
        column_names = get_column_names(pathcsv)
        # Perform operations with file_name if needed
        return render_template('forms.html', file_name=file_name, table_name=table_name, column_names=column_names, db_column_names=app.config['TABLE_CONFIG'][table_name])
    else:
        return "No file selected!", 400  # Or handle the case where no file name is provided



@app.route('/submit', methods=['POST'])
def submit():
    form_data = {}
    file = request.args.get('file', default=None) 
    print(request.form)
    for column in request.form:
        form_data[column] = request.form[column]
    #print(form_data)
    print(app.config['TABLE_CONFIG']['masterfile'])
    return redirect('/manage')

if __name__ == '__main__':
    app.run(debug=True)





'''
flask_csv_upload/
    |- app.py
    |- templates/
        |- upload.html
    |- data/
'''


"""
 Tables{masterdata:
    {
    item: pri
    description:normal
    prodfam:
    { fk_table: PRODFAM , fk_column: Prodfam} 
    }
        }
"""














































'''
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def get_column_names(csv_file):
    df = pd.read_csv(csv_file)
    return df.columns.tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # Check if no file was selected
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Check if the file is a CSV
        if file and file.filename.endswith('.csv'):
            column_names = get_column_names(file)

            return render_template('form.html', column_names=column_names)

    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    form_data = {}
    print(request.form)
    for column in request.form:
        form_data[column] = request.form[column]
    print(form_data)
    return 'Form submitted successfully!'


@app.route('/newindex', methods=['GET', 'POST'])
def newindex():
    tables = ['MASTERFILE', 'PRODFAM']

    return render_template('newindex.html', tables=tables)

if __name__ == '__main__':
    app.run(debug=True)

'''
