from flask import Flask, request, jsonify, render_template,send_from_directory
import os
import uuid
import cv2
import numpy as np
from PIL import Image
import imagehash

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

WATERMARK_TEXT = "MyInvisibleWatermark"

# Dictionary to store watermark hashes
watermark_hashes = {}

def add_watermark(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(output_path, fourcc, cap.get(5), (frame_width, frame_height))

    first_frame = None
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        overlay = frame.copy()
        cv2.putText(overlay, WATERMARK_TEXT, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

        if first_frame is None:
            first_frame = frame.copy()

        out.write(frame)

    cap.release()
    out.release()

    # Generate hash of first frame with watermark
    img = Image.fromarray(cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB))
    return str(imagehash.phash(img))

def detect_watermark(video_path, watermark_hash):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return False
    
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    video_hash = imagehash.phash(img)
    
    return abs(video_hash - imagehash.hex_to_hash(watermark_hash)) < 5  # Adjust threshold if needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400
    
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    video_id = str(uuid.uuid4())
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{video_id}.mp4')
    video.save(video_path)

    # Check watermark
    for wm_video_id, wm_hash in watermark_hashes.items():
        if detect_watermark(video_path, wm_hash):
            wm_video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'wm_{wm_video_id}.mp4')
            return jsonify({'message': 'Watermark detected!', 'video_url': wm_video_path})

    # If no watermark, add it
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'wm_{video_id}.mp4')
    stored_hash = add_watermark(video_path, output_path)
    watermark_hashes[video_id] = stored_hash  # Store the hash for future detection

    return jsonify({'message': 'No watermark found. Watermark added!', 'video_url': output_path})

@app.route('/detect_watermark', methods=['POST'])
def detect_watermark_route():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400
    
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    video_id = str(uuid.uuid4())
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{video_id}.mp4')
    video.save(video_path)

    # Check watermark
    for wm_video_id, wm_hash in watermark_hashes.items():
        if detect_watermark(video_path, wm_hash):
            wm_video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'wm_{wm_video_id}.mp4')
            return jsonify({'message': 'Watermark detected!', 'video_url': wm_video_path})

    return jsonify({'message': 'No watermark detected.'})
import os

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/videos_page')
def videos_page():
    return render_template('videos.html')

@app.route('/videos')
def get_videos():
    videos = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith('wm_') and filename.endswith('.mp4'):
            videos.append({
                'filename': filename,
                'url': f'{request.host_url}uploads/{filename}'  # Absolute URL
            })
    return jsonify(videos)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)