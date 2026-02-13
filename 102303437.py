#!/usr/bin/env python3
"""
Mashup CLI - 102303437.py
Author: Rohan Malhotra
Roll No: 102303437

Usage:
  python 102303437.py "<SingerName>" <NumberOfVideos> <AudioDurationSeconds> <OutputFileName>

Example:
  python 102303437.py "Sharry Maan" 20 20 102303437-output.mp3

Notes:
- Requires FFmpeg installed and available in PATH.
- Uses yt-dlp to download audio from YouTube search results.
"""

import os
import sys
import re
import shutil
import tempfile
from pathlib import Path

def print_usage():
    print('Usages: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>')
    print('Example: python 102303437.py "Sharry Maan" 20 20 102303437-output.mp3')

def is_positive_int(s: str) -> bool:
    try:
        return int(s) > 0
    except Exception:
        return False

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', '_', name.strip())
    name = re.sub(r'\s+', ' ', name).strip()
    return name or "output"

def ensure_ffmpeg():
    # A friendly check (not perfect) to catch missing ffmpeg early.
    from shutil import which
    if which("ffmpeg") is None:
        raise RuntimeError("FFmpeg not found in PATH. Please install FFmpeg and try again.")

def download_audios(query: str, n: int, out_dir: Path):
    """
    Downloads N audios from YouTube search results using yt-dlp.
    Outputs MP3 files into out_dir.
    """
    try:
        from yt_dlp import YoutubeDL
    except Exception as e:
        raise RuntimeError("Missing dependency yt-dlp. Install with: pip install yt-dlp") from e

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title).120s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "extractaudio": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        # Be a bit gentler:
        "retries": 3,
        "fragment_retries": 3,
    }

    search_term = f"ytsearch{n}:{query}"
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([search_term])
        except Exception as e:
            raise RuntimeError(f"Failed while downloading from YouTube for query: {query}") from e

    mp3s = sorted(out_dir.glob("*.mp3"))
    if len(mp3s) == 0:
        raise RuntimeError("No MP3 files were downloaded. Try a different singer name or check network.")
    return mp3s

def cut_and_merge(mp3_files, cut_seconds: int, output_path: Path):
    try:
        from pydub import AudioSegment
    except Exception as e:
        raise RuntimeError("Missing dependency pydub. Install with: pip install pydub") from e

    cut_ms = int(cut_seconds * 1000)
    segments = []
    for fp in mp3_files:
        try:
            audio = AudioSegment.from_file(fp)
            if len(audio) < cut_ms:
                seg = audio  # if shorter than requested, take full audio
            else:
                seg = audio[:cut_ms]
            segments.append(seg)
        except Exception as e:
            raise RuntimeError(f"Failed processing audio file: {fp.name}") from e

    if not segments:
        raise RuntimeError("No audio segments available to merge.")

    merged = segments[0]
    for seg in segments[1:]:
        merged += seg

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        merged.export(output_path, format="mp3")
    except Exception as e:
        raise RuntimeError(f"Failed exporting merged MP3: {output_path}") from e

def main():
    # Check parameters count
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print_usage()
        sys.exit(1)

    singer = sys.argv[1].strip()
    n_str = sys.argv[2].strip()
    y_str = sys.argv[3].strip()
    out_name = sys.argv[4].strip()

    # Validate inputs
    if not singer:
        print("Error: SingerName cannot be empty.")
        print_usage()
        sys.exit(1)

    if not is_positive_int(n_str):
        print("Error: NumberOfVideos must be a positive integer.")
        print_usage()
        sys.exit(1)

    if not is_positive_int(y_str):
        print("Error: AudioDuration must be a positive integer (seconds).")
        print_usage()
        sys.exit(1)

    n = int(n_str)
    y = int(y_str)

    if n <= 10:
        print("Error: NumberOfVideos must be > 10 as per assignment.")
        sys.exit(1)

    if y <= 20:
        print("Error: AudioDuration must be > 20 seconds as per assignment.")
        sys.exit(1)

    out_name = sanitize_filename(out_name)
    if not out_name.lower().endswith(".mp3"):
        out_name += ".mp3"

    output_path = Path.cwd() / out_name

    # Run
    try:
        ensure_ffmpeg()
        with tempfile.TemporaryDirectory(prefix="mashup_102303437_") as td:
            workdir = Path(td)
            print(f"[1/4] Downloading {n} videos for singer/query: {singer}")
            mp3s = download_audios(singer, n, workdir)

            print(f"[2/4] Converting completed (downloaded {len(mp3s)} mp3 files).")
            print(f"[3/4] Cutting first {y} seconds from each audio.")
            print(f"[4/4] Merging and exporting to: {output_path.name}")
            cut_and_merge(mp3s, y, output_path)

        print("✅ Done.")
        print(f"Output file: {output_path}")
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
