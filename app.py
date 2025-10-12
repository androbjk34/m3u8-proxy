from flask import Flask, request, redirect, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return '<h3>YouTube Proxy Çalışıyor ✅</h3><p>Kullanım: /youtube?id=VIDEO_ID</p>'

@app.route('/youtube')
def youtube():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Eksik id parametresi. ?id=VIDEO_ID"}), 400

    url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        ydl_opts = {"quiet": True, "format": "best"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info.get("url")
            if stream_url:
                return redirect(stream_url)
            else:
                return jsonify({"error": "Akış URL’si bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
