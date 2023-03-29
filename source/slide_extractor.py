import cv2
import numpy as np
from tqdm import tqdm

video_path = './video.mp4'
output_folder = './output'

cap = cv2.VideoCapture(video_path)

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

_, prev_frame = cap.read()
prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
frame_count = 0
keyframe_count = 0
threshold = 99  # You can adjust this value for better results

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Add a progress bar
with tqdm(total=total_frames, desc="Processing frames", unit="frame") as pbar:
    while cap.isOpened():
        ret, curr_frame = cap.read()

        if not ret:
            break

        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_frame_gray, curr_frame_gray)
        count = np.sum(diff > threshold)

        if count > 0:  # A major change is detected
            keyframe_count += 1

            # Save the keyframe as an image
            output_filename = f'{output_folder}/slide_{keyframe_count}.png'
            cv2.imwrite(output_filename, prev_frame)

        prev_frame = curr_frame.copy()
        prev_frame_gray = curr_frame_gray.copy()
        frame_count += 1

        pbar.update(1)

cap.release()
cv2.destroyAllWindows()
