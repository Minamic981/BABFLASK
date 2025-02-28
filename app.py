from flask import Flask, request, render_template, send_from_directory, jsonify, redirect
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
os.makedirs('uploads', exist_ok=True)
UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file', None)
    if not file:
        return jsonify({'error': 'file is missing'}), 401
    filename = secure_filename(file.filename)

    if filename == '':
        return jsonify({'error': 'filename cannot empty'}), 401
    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'url': f'/u/{filename}'}), 200

@app.route('/u/<path:filename>')
def u(filename):
    if not filename:
        return redirect('/')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/listfile', methods=['POST'])
def listfile():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/files')
def files():
    return render_template('files.html')

if __name__ == '__main__':
    app.run(port=7000, debug=True)