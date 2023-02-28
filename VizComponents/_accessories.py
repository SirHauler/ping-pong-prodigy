import glob
import os
import imageio.v2 as imageio
from datetime import datetime


def _make_video(picture_folder: str = "pictures", video_folder: str = "videos", prefix="default", fps: int = 60):
    # Makes the video from a directory of pictures
    nums = sorted([int(''.join(filter(str.isdigit, s))) for s in glob.glob(f'{picture_folder}/*.jpeg')])
    img_paths = [f'{picture_folder}/{n}_gameState.jpeg' for n in nums]
    if len(img_paths) == 0:
        raise ValueError(f'Didn\'t find any paths inside "\\{picture_folder}" folder.')

    # Loop through each JPEG image and add it to the writer object
    writer = imageio.get_writer(f'{video_folder}/{prefix}-{str(datetime.now())}.mp4', fps=fps)
    for image_file in img_paths:
        image = imageio.imread(image_file)
        writer.append_data(image)
    # Close the writer object to finalize the MP4 file
    writer.close()

    print(f"Made video in CWD.\n")

def _prepare_directory(picture_folder = "pictures", video_folder = "videos"):
    # PICTURES
    # Delete existing files in folder
    [os.remove(f) for f in glob.glob(f'{picture_folder}/*')]
    # Make folder if it doesn't exist
    os.makedirs(f'{picture_folder}') if not os.path.exists(f'{picture_folder}') else None
    print(f"Made \{picture_folder} in CWD.\n")

    # VIDEOS
    os.makedirs(f'{video_folder}') if not os.path.exists(f'{video_folder}') else None
    print(f"Made \{video_folder} in CWD.\n")