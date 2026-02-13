# Mashup Assignment (Program 1 + Program 2)

**Name:** Rohan Malhotra  
**Roll No:** 102303437  

This repo contains:

- **Program 1 (CLI):** `102303437.py`  
- **Program 2 (Web Service):** `webapp/` (Flask web app, Replit-ready)

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

## Program 2 (Web Service) - Replit Deployment

Open `webapp/` in Replit.

### Files
- `app.py` - Flask server
- `mashup.py` - mashup generator
- `mailer.py` - email sender via SMTP
- `replit.nix` - installs FFmpeg on Replit
- `requirements.txt` - python deps
- `templates/index.html` - UI

### Environment variables (Replit Secrets)
Set the following in Replit **Secrets**:
- `SMTP_HOST` (e.g. `smtp.gmail.com`)
- `SMTP_PORT` (e.g. `587`)
- `SMTP_USER` (your email)
- `SMTP_PASS` (Gmail App Password recommended)
- `FROM_EMAIL` (optional, default = SMTP_USER)

### Run
Replit should run:
```bash
python app.py
```

Then open the web URL, fill the form, and you’ll receive a ZIP file by email.

---

## Anti-plagiarism note
This code is written specifically for roll number **102303437** and uses a straightforward implementation with `yt-dlp` + `pydub`.
