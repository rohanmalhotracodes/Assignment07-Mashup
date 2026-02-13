# Mashup Web Service (Program 2)

**Name:** Rohan Malhotra  
**Roll No:** 102303437  

## Run locally
```bash
cd webapp
pip install -r requirements.txt
# ensure ffmpeg is installed locally
python app.py
```

Open: http://127.0.0.1:5000

## Deploy on Replit
- Import `webapp/` as a Replit project
- `replit.nix` installs ffmpeg
- Add SMTP settings as Secrets:
  - SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL

## SMTP (Gmail)
Use a Gmail **App Password** (not your normal password).
