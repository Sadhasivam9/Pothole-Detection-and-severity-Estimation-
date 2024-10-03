import io
import base64
from flask import Flask, Blueprint, render_template, request, redirect
from PIL import Image
import numpy as np
from ultralytics import YOLO
import base64


app = Flask(__name__)
app_blueprint = Blueprint('app', __name__)

# Load your YOLOv10 model
model = YOLO('models/best.pt')

@app_blueprint.route('/')
def index():
    return render_template('index.html')

@app_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Open the image file in memory
        img = Image.open(file.stream)

        # Process the image with the YOLO model
        results = model(img)

        # Convert NumPy array from results[0].plot() to PIL Image
        annotated_frame = results[0].plot()  # Get the annotated NumPy array
        img_pil = Image.fromarray(annotated_frame)  # Convert to PIL image

        # Convert the PIL image to bytes and then to base64 for display in HTML
        img_bytes = io.BytesIO()
        img_pil.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()
        encoded_img = base64.b64encode(img_bytes).decode('utf-8')

        return render_template('result.html', image_data=encoded_img)

if __name__ == '__main__':
    app.register_blueprint(app_blueprint)
    app.run(debug=True, host="0.0.0.0", port=5000)
