import datetime
import urllib3 as u
import urllib.parse
from flask import Flask, jsonify, redirect, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

@app.route('/')
def index():
    return "Home Page"

@app.route('/api/get_link')
def test2():
    url = request.args.get('url')
    # print(url)
    return url

@app.route('/api/summarize', methods=['GET'])
def summarized_sub():
    # url = request.args.get('url')
    script = show_transcripts()
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + script, return_tensors="pt", max_length=2048, truncation=True)
    outputs = model.generate(
                inputs, 
                max_length=150, 
                min_length=40, 
                length_penalty=2.0, 
                num_beams=4, 
                early_stopping=True
                )
    # print(tokenizer.decode(outputs[0]))
    return jsonify(summary = tokenizer.decode(outputs[0])), 200

@app.route('/api/transcript', methods=['GET'])
def show_transcripts():
    # url = request.args['url']
    url = "https://www.youtube.com/watch?v=dP15zlyra3c"
    url_data = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    video_id = query["v"][0]
    summary = ""
    sub = YouTubeTranscriptApi.get_transcript(video_id)
    for params in sub:
        # print(params['text'], end=' ')
        summary += params['text']
        summary += " "
    # print(summary)
    return jsonify(transcript = summary), 200

if __name__ == '__main__':
    app.run(port=8080, debug = True)