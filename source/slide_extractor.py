import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image
import os

def get_user_choice():
    print("Please choose the output mode:")
    print("1. Images")
    print("2. PDF")
    choice = input("Enter the number corresponding to your choice (1 or 2): ")

    while choice not in ['1', '2']:
        print("Invalid input. Please try again.")
        choice = input("Enter the number corresponding to your choice (1 or 2): ")

    return 'images' if choice == '1' else 'pdf'

# Set the input video file and output folder
video_path = './video.mp4'
output_folder = './output'
output_mode = get_user_choice()

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

_, prev_frame = cap.read()
prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

frame_count = 0
keyframe_count = 0
threshold = 99

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Initialize a list to store the keyframes for PDF output
if output_mode == 'pdf':
    keyframe_images = []

with tqdm(total=total_frames, desc="Processing frames", unit="frame") as pbar:
    while cap.isOpened():
        ret, curr_frame = cap.read()

        if not ret:
            break

        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_frame_gray, curr_frame_gray)
        count = np.sum(diff > threshold)

        if count > 0:
            keyframe_count += 1

            if output_mode == 'images':
                output_filename = f'{output_folder}/slide_{keyframe_count}.png'
                cv2.imwrite(output_filename, prev_frame)
            elif output_mode == 'pdf':
                keyframe_image = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2RGB)
                keyframe_images.append(Image.fromarray(keyframe_image))

        prev_frame = curr_frame.copy()
        prev_frame_gray = curr_frame_gray.copy()
        frame_count += 1

        pbar.update(1)

cap.release()
cv2.destroyAllWindows()

# Save the keyframes as a single PDF file
if output_mode == 'pdf' and keyframe_images:
    output_filename = f'{output_folder}/slides.pdf'
    keyframe_images[0].save(output_filename, save_all=True, append_images=keyframe_images[1:])
