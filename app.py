import datetime
from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
app.route('/')
def index_page():
    return "Yo"

app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.datetime.now())

def show_transcripts(str):
    import requests
    import json
    from youtube_transcript_api import YouTubeTranscriptApi

    sub = YouTubeTranscriptApi.get_transcript('YtIw3wqHeNY')
    for params in sub:
        print(params['text'], end=' ')


if __name__ == '__main__':
    app.run()