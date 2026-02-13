# Mashup Assignment

**Name:** Rohan Malhotra  
**Roll No:** 102303437  

This repo contains:

- **Program 1 (CLI):** `102303437.py`  
- **Program 2 (Web Service):** `webapp/`

---

## Program 1 (CLI)

### Install dependencies
```bash
pip install yt-dlp pydub
```

### FFmpeg requirement
FFmpeg must be installed and available in your PATH.

### Run
```bash
python 102303437.py "<SingerName>" <NumberOfVideos> <AudioDurationSeconds> <OutputFileName>
```

Example:
```bash
python 102303437.py "Sharry Maan" 20 20 102303437-output.mp3
```

---

## Program 2 – Mashup Web Service

This mashup web service is deployed on Render.

Deployed Link:
https://assignment07-mashup-2.onrender.com

## What it does

The web service takes the following inputs from the user:
- Singer name
- Number of videos (N > 10)
- Duration per clip in seconds (Y > 20)
- Email ID

It downloads N YouTube videos of the given singer, converts them to audio, trims the first Y seconds from each audio file, merges all clips into one mashup MP3, compresses the result into a ZIP file, and sends the ZIP file to the provided email address.

