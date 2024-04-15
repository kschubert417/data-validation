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

if __name__ == '__main__':
    app.run(debug=True)
