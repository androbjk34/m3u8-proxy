from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ M3U8 Proxy Çalışıyor! Kullanım: /proxy?url=http://...'

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "❌ Hata: 'url' parametresi eksik. Örnek: /proxy?url=http://...", 400

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Referer": request.host_url
    }

    try:
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        content_type = r.headers.get("Content-Type", "application/vnd.apple.mpegurl")
        
        def generate():
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    yield chunk

        resp = Response(generate(), content_type=content_type)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    except Exception as e:
        return f"❌ Proxy hatası: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
