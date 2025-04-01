# from ultralytics import YOLO

# # Load a model
# model = YOLO("yolo11l.pt")  # pretrained YOLO11n model

# # Run batched inference on a list of images
# results = model(["test.jpg","test2.jpg"])  # return a list of Results objects

# # Process results list
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen
#     result.save(filename="result.jpg")  # save to disk

import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11l.pt")  # pretrained YOLO11n model

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # 0 is the default camera index

if not cap.isOpened():
    raise ValueError("Could not open video source")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform inference on the current frame
    results = model(frame)  # return a list of Results objects

    # Process results list
    for result in results:
        annotated_frame = result.plot()  # Annotate the frame with detections

    # Display the resulting frame
    cv2.imshow('YOLO Detection', annotated_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

