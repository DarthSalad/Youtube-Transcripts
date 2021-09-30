import datetime
from flask import Flask, jsonify, redirect, request
from transformers import T5ForConditionalGeneration, T5Tokenizer
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/test')
def test():
    return "test success"

@app.route('/test2', methods=['POST', 'GET'])
def test2():
    url = request.form['link']
    return url

def summarized_sub(script):
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
    return tokenizer.decode(outputs[0])

@app.route('/api/summarize', methods=['GET'])
def show_transcripts():
    vid_id = input("Enter the YT link: ")[-11:]
    summary = ""
    sub = YouTubeTranscriptApi.get_transcript(vid_id)
    for params in sub:
        # print(params['text'], end=' ')
        summary += params['text']
        summary += " "
    # print(summary)
    summarized_sub(summary)

# show_transcripts(vid_id[-11:])

if __name__ == '__main__':
    app.run(debug = True)