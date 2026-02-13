import os
import re
import threading
import tempfile
import zipfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from mashup import generate_mashup_zip
from mailer import send_email_with_attachment

app = Flask(__name__)

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

def valid_int(s):
    try:
        return int(s)
    except:
        return None

def run_job(singer, n, dur, email):
    try:
        with tempfile.TemporaryDirectory(prefix="mashup_web_") as td:
            td = Path(td)
            zip_path = generate_mashup_zip(singer, n, dur, td, roll_no="102303437")
            subject = f"Mashup Result - 102303437"
            body = (
                f"Hi,\n\nYour mashup is ready.\n\n"
                f"Singer: {singer}\nVideos: {n}\nDuration: {dur}s\n\n"
                f"Regards,\nRohan Malhotra (102303437)\n"
            )
            send_email_with_attachment(
                to_email=email,
                subject=subject,
                body=body,
                attachment_path=zip_path
            )
    except Exception as e:
        # In a real system you'd persist logs; for assignment we print.
        print("JOB ERROR:", e, flush=True)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/generate")
def generate():
    singer = (request.form.get("singer") or "").strip()
    n = valid_int((request.form.get("videos") or "").strip())
    dur = valid_int((request.form.get("duration") or "").strip())
    email = (request.form.get("email") or "").strip()

    if not singer:
        return jsonify({"ok": False, "error": "Singer name is required."}), 400
    if n is None or n <= 10:
        return jsonify({"ok": False, "error": "Number of videos must be an integer > 10."}), 400
    if dur is None or dur <= 20:
        return jsonify({"ok": False, "error": "Duration must be an integer > 20 seconds."}), 400
    if not EMAIL_RE.match(email):
        return jsonify({"ok": False, "error": "Please enter a valid email address."}), 400

    # Safety caps for free hosting limits
    if n > 50:
        return jsonify({"ok": False, "error": "Max 50 videos allowed on this demo host."}), 400
    if dur > 60:
        return jsonify({"ok": False, "error": "Max duration per clip is 60 seconds on this demo host."}), 400

    t = threading.Thread(target=run_job, args=(singer, n, dur, email), daemon=True)
    t.start()

    return jsonify({"ok": True, "message": "Job started. You will receive a ZIP on email when ready."})

if __name__ == "__main__":
    # Replit uses 0.0.0.0 and PORT
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
