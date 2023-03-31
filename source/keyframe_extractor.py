import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tqdm import tqdm


def extract_keyframes(video_path, output_folder, threshold):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        messagebox.showerror("Error", "Error opening video file")
        return

    _, prev_frame = cap.read()
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    keyframe_count = 0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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
                output_filename = f'{output_folder}/slide_{keyframe_count}.png'
                cv2.imwrite(output_filename, prev_frame)

            prev_frame = curr_frame.copy()
            prev_frame_gray = curr_frame_gray.copy()
            frame_count += 1

            pbar.update(1)

    cap.release()
    cv2.destroyAllWindows()


def browse_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.flv;*.mov")])
    video_path_var.set(video_path)


def browse_output():
    output_folder = filedialog.askdirectory()
    output_folder_var.set(output_folder)


def start_processing():
    video_path = video_path_var.get()
    output_folder = output_folder_var.get()
    threshold = int(threshold_var.get())

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_keyframes(video_path, output_folder, threshold)
    messagebox.showinfo("Success", "Keyframes extraction completed")


root = tk.Tk()
root.title("Keyframe Extractor")

video_path_var = tk.StringVar()
output_folder_var = tk.StringVar()
threshold_var = tk.StringVar()

tk.Label(root, text="Video file:").grid(row=0, column=0, sticky=tk.W)
tk.Entry(root, textvariable=video_path_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_video).grid(row=0, column=2)

tk.Label(root, text="Output folder:").grid(row=1, column=0, sticky=tk.W)
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_output).grid(row=1, column=2)

tk.Label(root, text="Threshold:").grid(row=2, column=0, sticky=tk.W)
tk.Entry(root, textvariable=threshold_var, width=10).grid(row=2, column=1, sticky=tk.W)
threshold_var.set("99")

tk.Button(root, text="Extract Keyframes", command=start_processing).grid(row=3, column=1)

root.mainloop()
