import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from database import db, Candidate
from parser import extract_text_from_pdf, parse_resume

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/resume_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        raw_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(raw_text)
        
        new_candidate = Candidate(
            name=parsed_data['name'],
            email=parsed_data['email'],
            phone=parsed_data['phone'],
            skills=parsed_data['skills'],
            education=parsed_data['education']
        )
        db.session.add(new_candidate)
        db.session.commit()
        
        os.remove(file_path)
        
        return jsonify({
            "message": "Resume processed and saved successfully.",
            "data": parsed_data
        }), 201

    return jsonify({"error": "Invalid file format. Only PDF is supported."}), 400

@app.route('/candidates', methods=['GET'])
def get_candidates():
    skill_filter = request.args.get('skill')
    
    query = Candidate.query
    if skill_filter:
        query = query.filter(Candidate.skills.ilike(f'%{skill_filter}%'))
        
    candidates = query.all()
    return jsonify([c.to_dict() for c in candidates]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
