from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'videoId parameter missing'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return jsonify({'transcript': full_text})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcript not available for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
