from ultralytics import YOLO
import pytesseract
import cv2
import re

# Load the YOLO model
model = YOLO('best.pt')

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to process frames (common for video and image)
def process_frame(frame, plate_counter, detection_threshold):
    results = model.predict(frame, show=True)
    last_list = []

    for r in results:
        boxes = r.boxes.xyxy

        if len(boxes) > 0:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                cropped = frame[y1:y2, x1:x2]

                # Preprocess the cropped image
                gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (3, 3), 0)
                thresh = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                # Display the processed image (optional)
                cv2.imshow("Processed", thresh)

                # Extract text using Tesseract
                crop_img_text = pytesseract.image_to_string(thresh, lang='eng').strip()
                print(f"Extracted Text: {crop_img_text}")

                # Normalize and filter text
                crop_img_text = crop_img_text.strip().upper()  # Normalize text
                print(f"Normalized Text: {crop_img_text}")

                if len(crop_img_text) > 5 and re.match(r'^[A-Z0-9\s]+$', crop_img_text):
                    if crop_img_text in plate_counter:
                        plate_counter[crop_img_text] += 1
                    else:
                        plate_counter[crop_img_text] = 1

                    print(f"Plate Counter: {plate_counter}")

                    # Check against the threshold
                    if plate_counter[crop_img_text] >= detection_threshold:
                        if crop_img_text not in last_list:  # Avoid duplicates
                            last_list.append(crop_img_text)
                            print(f"Detected Plate: {crop_img_text}")

    # Filter duplicates and show detected plates
    print(f"Detected Plates: {last_list}")

# User choice for input type
input_type = input("Enter 'image' to upload an image or 'video' to upload a video: ").strip().lower()
plate_counter = {}

if input_type == 'image':
    detection_threshold = 1  # Immediate detection for images
    image_path = input("Enter the image file path: ").strip()
    frame = cv2.imread(image_path)
    if frame is not None:
        process_frame(frame, plate_counter, detection_threshold)
    else:
        print("Error: Unable to read the image file.")
    cv2.waitKey(0)

elif input_type == 'video':
    detection_threshold = 3  # Multiple detections required for videos
    video_path = input("Enter the video file path: ").strip()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open the video file.")
    else:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            process_frame(frame, plate_counter, detection_threshold)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()

else:
    print("Invalid input. Please enter 'image' or 'video'.")

# Close windows
cv2.destroyAllWindows()
