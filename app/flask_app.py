from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd

app = Flask(__name__)

# Folder where uploaded files will be stored
# print(os.getcwd())
upload_folder = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['TABLE_CONFIG'] = {'MASTERFILE':['ITEM', 'DESCRIPTION', 'ITEM_TYPE', 'PRODFAM'],
                              'PRODFAM':['PRODFAM', 'DESCRIPTION']}

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
    return redirect(url_for('manage'))

@app.route('/manage')
def manage():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    #return render_template('manage.html', files=files)
    return render_template('manage.html', files=files)

@app.route('/forms')
def forms():
    file_name = request.args.get('file', default=None)  # Get file name from query parameter
    # print(file_name)
    table_name = request.args.get('table', default=None)
    # print(f'TABLE NAME: {table_name}')
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
    # print(request.form)
    for column in request.form:
        form_data[column] = request.form[column]
    #print(form_data)
    # print(app.config['TABLE_CONFIG']['masterfile'])
    return redirect('/manage')

if __name__ == '__main__':
    app.run(debug=True)
