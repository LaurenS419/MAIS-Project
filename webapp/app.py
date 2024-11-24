import subprocess
from flask import Flask, render_template, request, url_for
import os
import cv2
import shutil

app = Flask(__name__)

@app.before_first_request
def install_dependencies():
    subprocess.run(["pip", "install", "torch==2.5.1", "torchvision==0.20.1"], check=True)

import torch

# Ensure the directories exist
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
FRAMES_FOLDER = 'static/frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['FRAMES_FOLDER'] = FRAMES_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)  # Recreate the directory after clearing

def process_video_with_yolo(input_path, output_video="processed_video.mp4"):
    
    # init YOLOv5 model with custom weights, change path as needed
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')
    
    cap = cv2.VideoCapture(input_path)
    second_rate = 2  # save frames every 2 seconds to avoid spam
    frame_dir = 'static/frames'
    confidence_cap = 0.6

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames_to_skip = int(fps * second_rate)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video_path = output_video # correct path for processed video
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    last_saved_frame = -frames_to_skip

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)  # object detection

        filtered_results = []
        for i, (xmin, ymin, xmax, ymax, confidence, class_idx) in enumerate(results.xyxy[0]):
            label = model.names[int(class_idx)]
            if confidence > confidence_cap and label in {"car", "person", "animal"}:
                filtered_results.append((xmin, ymin, xmax, ymax, confidence, class_idx))

        # render filtered results on frame
        for xmin, ymin, xmax, ymax, confidence, class_idx in filtered_results:
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            cv2.putText(frame, f"{model.names[int(class_idx)]} {confidence:.2f}", 
                        (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        out.write(frame)

        # save frames every second_rate seconds
        if frame_count - last_saved_frame >= frames_to_skip and filtered_results:
            last_saved_frame = frame_count
            frame_filename = f'{frame_dir}/frame_{frame_count:04d}.jpg'
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()
    out.release()

    # converts it into a format that works on webpages
    converted_video = "static/processed/processed_video_fixed.mp4"
    converted_video_name = "processed_video_fixed.mp4"
    subprocess.run([
        "ffmpeg", "-i", output_video, 
        "-vcodec", "libx264", "-acodec", "aac", converted_video,
        "-y"  # overwrite if file exists
    ])
    
    return converted_video_name, frame_dir


@app.route('/')
def index():
    # Clear the directories before rendering the page
    clear_directory(app.config['PROCESSED_FOLDER'])
    clear_directory(app.config['FRAMES_FOLDER'])
    clear_directory(app.config['UPLOAD_FOLDER'])
    
    return render_template('index.html', video_urls=None, frames=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    # clear directories before processing new video
    clear_directory(app.config['PROCESSED_FOLDER'])
    clear_directory(app.config['FRAMES_FOLDER'])
    clear_directory(app.config['UPLOAD_FOLDER'])

    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        original_filename = file.filename
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_path)

        # process video
        processed_filename, frame_dir = process_video_with_yolo(original_path, os.path.join(app.config['PROCESSED_FOLDER'], 'processed_video.mp4'))

        video_urls = {
            'original': url_for('static', filename=f'uploads/{original_filename}'),
            'processed': url_for('static', filename=f'processed/{processed_filename}')
        }

        frame_urls = [url_for('static', filename=f'static/frames/{frame}') for frame in os.listdir(frame_dir)]

        return render_template('index.html', video_urls=video_urls, frames=frame_urls)

    return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(debug=True)
