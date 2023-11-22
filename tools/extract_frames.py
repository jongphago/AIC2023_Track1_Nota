import os
import subprocess
from pathlib import Path
from tqdm import tqdm
import argparse


def make_parser():
    parser = argparse.ArgumentParser("Extrafct Frames from AIC23 Track1 Videos")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=None,
        help="path to AIC23_Track1_MTMC_Tracking folder",
    )
    return parser.parse_args()


def extract_frames(video_file, output_folder, file_headname):
    # Use ffmpeg to extract frames from the video file
    command = [
        "ffmpeg",
        "-ss",
        "00:02:39",
        "-i",
        video_file,
        "-r",
        "30",
        # '-vf',
        "-q",
        "2",
        "-f",
        "image2",
        "-frames",
        "100",
        os.path.join(output_folder, file_headname + "_%d.jpg"),
    ]
    print(command)
    subprocess.run(command)


def main(path):
    # videos = Path(os.path.join(path, "test")).glob("**/*.mp4")
    videos = Path(path).glob("**/c0*/*.avi")

    for vid in tqdm(videos):
        output_folder = f"./datasets/{vid.parts[-3]}/{vid.parts[-2]}"
        os.makedirs(output_folder, exist_ok=True)
        file_headname = vid.parts[-3] + vid.parts[-2]
        print(file_headname)
        extract_frames(str(vid), output_folder, file_headname)


if __name__ == "__main__":
    args = make_parser()
    main(args.path)