import os
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import torch
from ultralytics import YOLO
import cv2

app = Blueprint('app', __name__)

# Load your YOLOv10 model
model = YOLO('models/best.pt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Secure the filename and save it
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.root_path, 'static', 'uploads', filename)
        file.save(upload_path)

        # Process the file based on whether it's an image or a video
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Process image
            results = model(upload_path)
            result_image_path = os.path.join(app.root_path, 'static', 'results', 'result_' + filename)
            results[0].save(result_image_path)
            return render_template('result.html', filename='result_' + filename)
        
        elif filename.lower().endswith(('.mp4', '.avi', '.mov')):
            # Process video
            output_path = os.path.join(app.root_path, 'static', 'results', 'result_' + filename.split('.')[0] + '.mp4')
            process_video(upload_path, output_path)
            return render_template('result.html', filename='result_' + filename.split('.')[0] + '.mp4')
        
        else:
            return 'Unsupported file format'

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    # Use the 'avc1' codec (H.264) for broad browser compatibility
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)  # Run inference on each frame
        annotated_frame = results[0].plot()  # Annotate the frame
        out.write(annotated_frame)  # Save the annotated frame
    
    cap.release()
    out.release()

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.root_path, 'static', 'results', filename), as_attachment=True)

# Route to serve the video directly
@app.route('/video/<filename>')
def serve_video(filename):
    return send_file(os.path.join(app.root_path, 'static', 'results', filename), mimetype='video/mp4')
