
Face Recognition Attendance System
Deployed Demo:

Attendance Upload

Student Registration

Attendance Table

Table of Contents
Project Overview

Installation

Usage

Technologies

Features

Screenshot

Deployment Mode

License

Project Overview
A cloud-based face recognition attendance system using Python, Flask, and the face_recognition library. Supports live registration, attendance marking by face upload, and reporting. Any device/browser supported.

Installation
Clone/download the repository:

bash
git clone https://github.com/yourusername/face-attendance-flask.git
cd face-attendance-flask
Set up a Python environment:

bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Usage
Run the app:

bash
python attendance_api.py
Open in browser:

Registration: http://127.0.0.1:5000/register

Attendance upload: http://127.0.0.1:5000/upload

Table/report: http://127.0.0.1:5000/attendance_html

Technologies
Python 3.x

Flask

face_recognition

pandas

numpy

Features
Dynamic Registration: Add new students with a name and face photo.

Attendance Marking: Upload a face photo for instant attendance marking.

Reporting: HTML table for easy print/screenshot.

Mobile/Desktop Supported: Works on any browser/device.

Screenshot
<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/a631ba5c-476b-4d44-a548-a5fd660d02a0" />
<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/d88f5b7b-9d01-4ee2-b79e-9acb75e30fb5" />
<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/faeebd61-b509-4235-b049-bc325b451154" />

**Deployment Mode**
PythonAnywhere PaaS Cloud Platform

Why chosen: Simple setup, reliable, and accessible for students. Free tier available, no manual server maintenance needed. Perfect for academic projects and demos.

