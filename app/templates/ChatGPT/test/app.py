from flask import Flask, request, render_template, redirect, url_for, session
import os
import pandas as pd
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key'  # Should be a secure, unique key

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        
        if not files:
            return 'No file uploaded!', 400
        
        # Save files and generate session ID for this batch
        session_id = str(uuid.uuid4())
        session['files'] = []
        
        for file in files:
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                session['files'].append(filepath)
        
        session['session_id'] = session_id
        return redirect(url_for('list_files', session_id=session_id))
    
    return render_template('upload.html')

@app.route('/files/<session_id>')
def list_files(session_id):
    if 'session_id' not in session or session['session_id'] != session_id:
        return redirect(url_for('upload_file'))
    
    files = session['files']
    print(files)
    return render_template('file_view.html', files=files)

@app.route('/view/<path:filename>')
def view_file(filename):
    data = pd.read_csv(filename)
    columns = data.columns.tolist()
    return render_template('file_view.html', columns=columns, filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.3")
