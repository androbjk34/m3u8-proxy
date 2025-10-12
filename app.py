from flask import Flask, request, redirect, jsonify
import yt_dlp
import os

app = Flask(__name__)

COOKIE_FILE = "youtube_cookies.txt"

@app.route('/')
def home():
    return "YouTube IPTV Proxy with Cookies is running!"

@app.route('/stream')
def stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Eksik parametre ?id="}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best[ext=m3u8]/best",
        "cookiefile": COOKIE_FILE
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            for f in formats:
                if f.get("protocol") == "m3u8_native":
                    return redirect(f["url"])
            return jsonify({"error": "m3u8 link bulunamadı"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
