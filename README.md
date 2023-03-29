# SlideExtractor

A Python script to extract presentation slides from video files using OpenCV.

## Overview

SlideExtractor is a tool designed to help users extract keyframes (presentation slides) from video recordings of lectures, courses, or presentations. The script detects major changes between consecutive video frames and assumes that a significant change indicates a new slide. These keyframes are then saved as individual image files.

## Prerequisites

- Python 3.6 or higher
- OpenCV (opencv-python)
- tqdm

## Installation

1. Install Python 3.6 or higher if you haven't already.
2. Clone the SlideExtractor repository or download it as a zip file and extract it.
3. Install the required libraries using pip:

pip install opencv-python tqdm


## Usage

1. Open `slide_extractor.py` and modify the following variables to specify your input video file and output folder:

```python
video_path = '/path/to/your/video.mp4'
output_folder = '/path/to/output/folder'
```

Replace /path/to/your/video.mp4 with the path to your video file and /path/to/output/folder with the path to the folder where you want to save the extracted slides.

2. Adjust the threshold variable to fine-tune the slide detection sensitivity if needed:

```python
threshold = 50  # You can adjust this value for better results
```

A higher threshold value will make the script less sensitive to changes between frames, while a lower value will make it more sensitive. Experiment with different values to find the optimal threshold for your video.

3. Run the script:

```python
python slide_extractor.py
```

The script will process the video and save the extracted slides as image files in the specified output folder.
