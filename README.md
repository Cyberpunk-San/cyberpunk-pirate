# 🎥 CYBERPUNK-PIRATES 🚀

## 🔹 Project Overview
This project is a powerful **video protection system** that prevents piracy through **invisible watermarking, piracy detection, and real-time screen recording prevention**. Unlike traditional DRM solutions, this approach ensures that unauthorized screen recordings are rendered **completely useless** by displaying a blank screen or funny memes instead of the actual video! 🎭

## ✨ Key Features
- 🔍 **Invisible Watermarking** – Embeds hidden watermarks to track and identify reuploaded pirated content.
- 🎬 **Screen Recording Detection** – Detects when a user attempts to record the screen and instantly replaces the video with a blank screen or memes.
- 🚫 **Piracy Prevention** – Uses advanced fingerprinting techniques like **Perceptual Hashing (pHash)** and **Audio Fingerprinting (Chromaprint)** to detect copyrighted content.
- ⚡ **Lightweight & Efficient** – No cloud-based DRM or complex security infrastructure needed—making it **fast, flexible, and easy to integrate!**

## 🛠 Technologies Used
- **Frontend:** HTML, CSS, JavaScript (for UI interactions)
- **Backend:** Python (Flask) for video processing and piracy detection
- **Video Processing:** OpenCV and FFmpeg for watermarking and detection
- **Screen Recording Detection:** JavaScript APIs (`document.visibilityState`, UI manipulation tricks)
- **Piracy Detection:** Perceptual Hashing (pHash), Audio Fingerprinting (Chromaprint)

## 🚀 Installation & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/video-protection-system.git
   cd video-protection-system
   ```
2. Install dependencies:
   ```sh
   pip install flask opencv-python ffmpeg-python chromaprint
   ```
3. Run the Flask server:
   ```sh
   python app.py
   ```
4. Open `index.html` in a browser to test the system.

## 🎯 How It Works
- **Uploading Videos:** Users can upload videos, and the system will check for copyright violations before adding an invisible watermark.
- **Watching Videos:** If screen recording is detected, the video will be replaced with a blank screen or meme. 🤡
- **Piracy Detection:** The system checks uploaded videos for piracy using advanced fingerprinting techniques.

