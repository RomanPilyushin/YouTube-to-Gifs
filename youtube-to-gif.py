#!/usr/bin/env python

import subprocess
import sys
import os

def download_video(youtube_url, output_path):
    """
    Download a YouTube video using yt-dlp.

    Args:
    - youtube_url: URL of the YouTube video to download.
    - output_path: Path to save the downloaded video.
    """
    subprocess.run(['yt-dlp', '-o', output_path, youtube_url])


def convert_to_gif(video_path, output_path, start_time=0, duration=None, fps=10):
    """
    Convert a video to GIF using ffmpeg.

    Args:
    - video_path: Path to the input video file.
    - output_path: Path to save the generated GIF.
    - start_time: Start time of the video to capture (in seconds).
    - duration: Duration of the video to capture (in seconds). If None, capture until the end.
    - fps: Frames per second for the GIF.
    """
    cmd = ['ffmpeg', '-y', '-ss', str(start_time), '-i', video_path]
    if duration is not None:
        cmd.extend(['-t', str(duration)])
    cmd.extend(
        ['-vf', f'fps={fps},scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_path])
    subprocess.run(cmd)


def optimize_gif(input_path, output_path):
    """
    Optimize a GIF using gifsicle.

    Args:
    - input_path: Path to the input GIF file.
    - output_path: Path to save the optimized GIF.
    """
    subprocess.run(['gifsicle', '--optimize=3', input_path, '-o', output_path])


def delete_video(video_path):
    """
    Delete the video file.

    Args:
    - video_path: Path to the video file to be deleted.
    """
    os.remove(video_path)


def delete_temp_gif(temp_gif_path):
    """
    Delete the temporary GIF file.

    Args:
    - temp_gif_path: Path to the temporary GIF file to be deleted.
    """
    os.remove(temp_gif_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python youtube-to-gif.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    video_output_path = "video.webm"

    download_video(youtube_url, video_output_path)
    convert_to_gif(video_output_path, "temp.gif")
    optimize_gif("temp.gif", "result.gif")
    delete_video(video_output_path)
    delete_temp_gif("temp.gif")
    print("GIF generation complete!")
