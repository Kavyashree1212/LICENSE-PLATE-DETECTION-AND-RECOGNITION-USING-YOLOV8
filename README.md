# LICENSE-PLATE-DETECTION-AND-RECOGNITION-USING-YOLOV8
Real-time number plate detection and recognition using YOLOv8 + Tesseract OCR."

This project uses **YOLOv8** for license plate detection and **Tesseract OCR** for text recognition.  
It can process both **images** and **videos** in real time.

## Features
- Detects number plates using YOLOv8
- Extracts text from plates using Tesseract OCR
- Supports both image and video input
- Configurable detection threshold to reduce false positives
- (Optional) Save recognized plates into an SQLite database

## Installation
```bash
git clone https://github.com/Kavyashree1212/LICENSE-PLATE-DETECTION-AND-RECOGNITION-USING-YOLOV8.git
cd LICENSE-PLATE-DETECTION-AND-RECOGNITION-USING-YOLOV8
pip install -r requirements.txt
