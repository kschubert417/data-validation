import os
import json
import pandas as pd

from threading import Lock
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, jsonify
from tables import dbsetup
from tables.masterfile import masterfile
from tables.product_family import product_family


app = Flask(__name__)

# app.config['SECRET_KEY'] = 'your-secret-key
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
metadata = {}
metadata_lock = Lock()
# Folder where uploaded files will be stored based on computer
if os.getenv('COMPUTERNAME') == 'DESKTOP-3U5BV0O':
    upload_folder = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    dbfile = os.path.join(os.getcwd(), 'app', 'schema.db')
else:
    upload_folder = os.path.join('static', 'uploads') # removed os.getcwd() and 'app' because in my machine it does not work. This runs in app so just using relative paths here
    dbfile = os.path.join(os.getcwd(), 'app', 'schema.db')

# print(upload_folder)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['TABLE_CONFIG'] = {'MASTERFILE':['ITEM', 'DESCRIPTION', 'ITEM_TYPE', 'PRODFAM'],
                              'PRODFAM':['PRODFAM', 'DESCRIPTION']}



def clear_metadata():
    """Clear metadata dictionary."""
    with metadata_lock:
        metadata.clear()



def add_file_metadata(file_name, table_name, column_names):
    """Add file metadata into global dictionary."""
    # Find way to make session, this could be shared all over place
    with metadata_lock:
        metadata[file_name] = {
            "table_name": table_name,
            "column_names": column_names,
            "column_mapping": {}
        }


def get_column_names(csv_file):
    # print(f'CSV FILE: {csv_file}')
    # csv_file = os.path.join(upload_folder, 'masterdata.csv')
    df = pd.read_csv(csv_file)
    # print(df.columns.tolist())
    return df.columns.tolist()

@app.route('/', methods=['GET'])
def index():
    # print(app.config)
    return render_template('index.html')


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/customerconfig', methods=['GET', 'POST'])
def customerconfig():
    customer = request.args.get("customer", default=None)
    swvendor = request.args.get("swvendor", default=None)
    print(f"Customer: {customer} | Vendor: {swvendor}")
    return render_template('customerconfig.html', customer=customer, swvendor=swvendor)


@app.route('/upload', methods=['GET','POST'])
def upload_files():
    uploaded_files = request.files.getlist("file[]")
    for file in uploaded_files:
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            # print(f'PRINTING FILE PATH: {filepath}')
            file.save(filepath)
            # column_names = get_column_names(file.filename)
            column_names = get_column_names(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            table_name = None
            add_file_metadata(file.filename, table_name, column_names)
    # print('---\n','metadata from "/upload"', metadata,'\n------------\n')
    return redirect(url_for('manage'))



@app.route('/manage', methods=['GET'])
def manage():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # print('PRINT METADATA \n', metadata)
    #return render_template('manage.html', files=files, )
    return render_template('manage.html', files=files, db_table_names=app.config['TABLE_CONFIG'], metadata=metadata)

@app.route('/save', methods=['GET','POST'])
def save():
    #file_name = request.args.get('file', default=None)
    if request.is_json:
        data = request.get_json()
        # print('json', type(data))
    else:
        data = request.form.to_dict()
        # print('dictionary', type(data))
    if request.args.get('file', default=None):
        file_name = request.args.get('file', default=None)
        metadata[file_name]['column_mapping'].update(data)
    #print("Received data:", data)  # This will print the data to the server console
    # print(metadata)
    files = [ i for i in metadata]
    # print(files)
    return render_template('manage.html', files=files, metadata=metadata, db_table_names=app.config['TABLE_CONFIG'])

@app.route('/forms')
def forms():
    # print('in forms before updating table name',metadata)
    file_name = request.args.get('file', default=None)  # Get file name from query parameter
    # print(file_name)
    table_name = request.args.get('table', default=None)
    # print(table_name)
    metadata[file_name]['table_name'] = table_name
    # print('in forms after updating table name',metadata)
    if file_name:
        pathcsv = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        column_names = get_column_names(pathcsv)
        # Perform operations with file_name if needed
        return render_template('forms.html', metadata = metadata,file_name=file_name, table_name=table_name, column_names=column_names, db_column_names=app.config['TABLE_CONFIG'][table_name])
    else:
        return "No file selected!", 400  # Or handle the case where no file name is provided


@app.route('/validate', methods=['GET'])
def validate():
    dbsetup.cleardb(dbfile)
    dbsetup.dbsetup(dbfile)

    # Going through files to import data
    for file in metadata:
        print(file)
        order = []
        # print(file)
        # print(x[file]['column_mapping'])
        filcol = metadata[file]['column_mapping']
        for col in filcol:
            # print(y[col])
            order.append(filcol[col])

        # Finding tables that need to be inserted into database
        if metadata[file]['table_name'] == 'MASTERFILE':
            mf = masterfile()
            mf.createtable(dbfile)
            mf.insertdata(os.path.join(upload_folder, file), dbfile, order)
        elif metadata[file]['table_name'] == 'PRODFAM':
            pf = product_family()
            pf.createtable(dbfile)
            pf.insertdata(os.path.join(upload_folder, file), dbfile, order)

    # Going through files again to perform analysis
    for file in metadata:
        if metadata[file]['table_name'] == 'MASTERFILE':
            mf.basiccheck(dbfile)
            mf.fkcheck(dbfile)
        elif metadata[file]['table_name'] == 'PRODFAM':
            pf.basiccheck(dbfile)

    # Getting data to display
    return render_template('sum_stats.html', table_data=dbsetup.table_summary_stats(dbfile), data=dbsetup.get_summary_stats(dbfile))


@app.route('/table_error', methods=['GET'])
def table_error():
    table = request.args.get("table", default=None)
    error_data = dbsetup.specific_table_errors(dbfile, table)
    return render_template('table_stats.html', error_data=error_data, table=table)


if __name__ == '__main__':
    app.run(debug=True)
