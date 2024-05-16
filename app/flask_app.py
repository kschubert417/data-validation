from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import pandas as pd
from threading import Lock


app = Flask(__name__)

# app.config['SECRET_KEY'] = 'your-secret-key
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
metadata = {}
metadata_lock = Lock()
# Folder where uploaded files will be stored
upload_folder = os.path.join( 'static', 'uploads') # removed os.getcwd() and 'app' because in my machine it does not work. This runs in app so just using relative paths here
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['TABLE_CONFIG'] = {'MASTERFILE':['ITEM', 'DESCRIPTION', 'ITEM_TYPE', 'PRODFAM'],
                              'PRODFAM':['PRODFAM', 'DESCRIPTION']}

'''
session['files'] = {'masterdata.csv':{'MASTERFILE':[]},
                    'prodfam.csv':{'PRODFAM':[]}}
'''

''''''
def clear_metadata():
    """Clear metadata dictionary."""
    with metadata_lock:
        metadata.clear()



def add_file_metadata(file_name, table_name, column_names):
    """Add file metadata into global dictionary."""
    with metadata_lock:
        metadata[file_name] = {
            "table_name": table_name,
            "column_names": column_names,
            "column_mapping": {}
        }

def get_column_names(csv_file):
    df = pd.read_csv(csv_file)
    return df.columns.tolist()

@app.route('/')
def index():
    # print(app.config)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("file[]")
    for file in uploaded_files:
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            column_names = get_column_names(file.filename)
            if file.filename == 'masterdata.csv':
                table_name = None  # Example default table name
            elif file.filename == 'prodfam_data.csv':
                table_name = None
            add_file_metadata(file.filename, table_name, column_names)
    print('metadata from "/upload"', metadata,'\n\n\n\n\n\n')

    return redirect(url_for('manage'))

@app.route('/manage')
def manage():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    print('metadata from "/manage"', metadata)
    #return render_template('manage.html', files=files)
    return render_template('manage.html', files=files)

@app.route('/forms')
def forms():
    print('in forms before updating table name',metadata)
    file_name = request.args.get('file', default=None)  # Get file name from query parameter
    # print(file_name)
    table_name = request.args.get('table', default=None)
    metadata[file_name]['table_name'] = table_name
    print('in forms after updating table name',metadata)
    if file_name:
        pathcsv = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        column_names = get_column_names(pathcsv)
        # Perform operations with file_name if needed
        return render_template('forms.html', metadata = metadata,file_name=file_name, table_name=table_name, column_names=column_names, db_column_names=app.config['TABLE_CONFIG'][table_name])
    else:
        return "No file selected!", 400  # Or handle the case where no file name is provided


@app.route('/submit', methods=['GET','POST'])
def submit():
    file = request.args.get('file', default=None)
    print(f'metadata for {file} in ',metadata[file])
    '''
    for column in metadata[file]['column_names']:
        print(column)
        print(request.form[column])
    #for column in request.form:
        #form_data[column] = request.form[column]
    #print(form_data)
    # print(app.config['TABLE_CONFIG']['masterfile'])
    #print(form_data)
    '''
    return redirect('/manage')

if __name__ == '__main__':
    app.run(debug=True)
