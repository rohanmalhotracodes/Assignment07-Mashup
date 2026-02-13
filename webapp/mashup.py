import re
from pathlib import Path

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', '_', name.strip())
    name = re.sub(r'\s+', ' ', name).strip()
    return name or "output"

def ensure_ffmpeg():
    from shutil import which
    if which("ffmpeg") is None:
        raise RuntimeError("FFmpeg not found in PATH. On Replit, use the provided replit.nix to install it.")

def download_audios(query: str, n: int, out_dir: Path):
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
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ],
        "retries": 3,
        "fragment_retries": 3,
    }

    search_term = f"ytsearch{n}:{query}"
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_term])

    mp3s = sorted(out_dir.glob("*.mp3"))
    if not mp3s:
        raise RuntimeError("No MP3 files were downloaded.")
    return mp3s

def cut_and_merge(mp3_files, cut_seconds: int, output_path: Path):
    try:
        from pydub import AudioSegment
    except Exception as e:
        raise RuntimeError("Missing dependency pydub. Install with: pip install pydub") from e

    cut_ms = int(cut_seconds * 1000)
    segments = []
    for fp in mp3_files:
        audio = AudioSegment.from_file(fp)
        seg = audio[:cut_ms] if len(audio) >= cut_ms else audio
        segments.append(seg)

    merged = segments[0]
    for seg in segments[1:]:
        merged += seg

    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.export(output_path, format="mp3")

def generate_mashup_zip(singer: str, n: int, dur: int, workdir: Path, roll_no: str = "102303437") -> Path:
    ensure_ffmpeg()
    dl_dir = workdir / "downloads"
    dl_dir.mkdir(parents=True, exist_ok=True)

    mp3s = download_audios(singer, n, dl_dir)

    out_mp3 = workdir / f"{roll_no}-{sanitize_filename(singer)}-mashup.mp3"
    cut_and_merge(mp3s, dur, out_mp3)

    zip_path = workdir / f"{roll_no}-mashup.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(out_mp3, arcname=out_mp3.name)

    return zip_path
