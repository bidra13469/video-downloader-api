from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'الرجاء إدخال رابط'}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            download_options = []

            for fmt in formats:
                if fmt.get('vcodec') != 'none':
                    download_options.append({
                        'url': fmt['url'],
                        'quality': fmt.get('format_note', 'unknown'),
                        'extension': fmt.get('ext', 'mp4'),
                        'type': 'video'
                    })
                elif fmt.get('acodec') != 'none':
                    download_options.append({
                        'url': fmt['url'],
                        'quality': fmt.get('format_note', 'audio'),
                        'extension': fmt.get('ext', 'mp3'),
                        'type': 'audio'
                    })

            return jsonify({
                'title': info.get('title', 'Untitled'),
                'medias': download_options,
                'error': False
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)