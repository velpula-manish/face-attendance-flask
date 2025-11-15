from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import face_recognition
import numpy as np
import os
from datetime import datetime
FACE_DISTANCE_THRESHOLD = 0.5

app = Flask(__name__)
CORS(app)

# Load known faces from your faces directory
def load_known_faces():
    enc, names = [], []
    if not os.path.exists("faces"):
        return enc, names
    for folder in os.listdir("faces"):
        name = folder.strip()
        if not name:
            continue
        for imgf in os.listdir(os.path.join("faces", folder)):
            imp = os.path.join("faces", folder, imgf)
            try:
                im = face_recognition.load_image_file(imp)
                encoding = face_recognition.face_encodings(im)
                if encoding:
                    enc.append(encoding[0])
                    names.append(name)
            except Exception:
                pass
    return enc, names

# Mark attendance in the CSV for a recognized name
def mark_period(name):
    PERIODS = [f"{h}:00-{h+1}:00" for h in range(0, 24)]

    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    hour = now.hour
    idx = hour - 9
    if 0 <= idx < len(PERIODS):
        period_col = PERIODS[idx]
        if os.path.exists('attendance.csv'):
            df = pd.read_csv('attendance.csv')
        else:
            columns = ["Name", "Date"] + PERIODS
            df = pd.DataFrame([[name, today] + ['Absent']*len(PERIODS)], columns=columns)
        row = (df["Name"] == name) & (df["Date"] == today)
        if not row.any():
            new_row = pd.DataFrame([[name, today] + ['Absent']*len(PERIODS)], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            row = (df["Name"] == name) & (df["Date"] == today)
        df.loc[row, period_col] = 'Present'
        df.to_csv('attendance.csv', index=False)
        return f"{name} marked Present for {period_col}"
    return f"Not in college hours (9-17)."

@app.route('/')
def index():
    return "Face Recognition Attendance API Running"



@app.route('/mark', methods=['POST'])
def mark():
    if 'file' not in request.files:
        return jsonify({'status': 'fail', 'reason': 'No file uploaded'}), 400
    img_file = request.files['file']
    img = face_recognition.load_image_file(img_file)
    encodings = face_recognition.face_encodings(img)
    known_face_encodings, known_face_names = load_known_faces()
    for encoding in encodings:
        face_distances = face_recognition.face_distance(known_face_encodings, encoding)
        if len(face_distances) == 0:
            continue
        best_match_idx = np.argmin(face_distances)
        if face_distances[best_match_idx] < FACE_DISTANCE_THRESHOLD:
            name = known_face_names[best_match_idx]
            result = mark_period(name)
            return jsonify({'status': 'success', 'name': name, 'result': result})
    return jsonify({'status': 'fail', 'reason': 'Face not recognized'})

@app.route('/attendance', methods=['GET'])
def fetch_attendance():
    if not os.path.exists('attendance.csv'):
        return jsonify([])
    df = pd.read_csv('attendance.csv')
    today = datetime.now().strftime('%Y-%m-%d')
    df = df[df['Date'] == today]
    return df.to_json(orient='records')
@app.route('/attendance_html')
def view_attendance_html():
    import pandas as pd, os
    if not os.path.exists('attendance.csv'):
        return "<h3>No records found.</h3>"
    df = pd.read_csv('attendance.csv')
    html = df.to_html(index=False, border=1, classes='attendance-table')
    style = """
      <style>.attendance-table { border-collapse:collapse; margin:20px 0; }
      .attendance-table th, .attendance-table td { border:1px solid #666; padding:7px 15px; }
      .attendance-table th { background:#eeeeff; }</style>"""
    button = '<button onclick="window.print()">Print / Save as PDF</button>'
    return style + button + html

from flask import render_template

@app.route('/upload', methods=['GET', 'POST'])
def upload_attendance():
    FACE_DISTANCE_THRESHOLD = 0.5
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', result="No file uploaded.", status='fail')
        file = request.files['file']
        if file and file.filename.lower().endswith(('.jpg','.jpeg')):
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)
            known_encodings, known_names = load_known_faces()
            for encoding in encodings:
                face_distances = face_recognition.face_distance(known_encodings, encoding)
                if len(face_distances) == 0:
                    continue
                best_match_idx = np.argmin(face_distances)
                if face_distances[best_match_idx] < FACE_DISTANCE_THRESHOLD:
                    name = known_names[best_match_idx]
                    result = mark_period(name)
                    return render_template('upload.html', result=f"{result} ({name})", status='success')
            return render_template('upload.html', result="Face not recognized.", status='unknown')
        else:
            return render_template('upload.html', result="Invalid file type.", status='fail')
    return render_template('upload.html')
@app.route('/register', methods=['GET', 'POST'])
def register_student():
    import os
    if request.method == 'POST':
        name = request.form.get('student_name', '').strip()
        file = request.files.get('face_file', None)
        if not name:
            return render_template('register.html', result="Name is required.")
        if not file or not file.filename.lower().endswith(('.jpg', '.jpeg')):
            return render_template('register.html', result="Valid image required.", status='fail')
        # Prepare the folder for the student
        person_folder = os.path.join('faces', name)
        os.makedirs(person_folder, exist_ok=True)
        # Save the uploaded image to that folder
        file.save(os.path.join(person_folder, file.filename))
        return render_template('register.html', result=f"Student '{name}' registered!")
    return render_template('register.html')

