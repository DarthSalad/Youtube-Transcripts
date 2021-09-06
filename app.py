import datetime
from flask import Flask, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/summarize/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/')
def index_page():
    return "test success"

@app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.datetime.now())

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
    print(tokenizer.decode(outputs[0]))

def show_transcripts(video_id):
    summary = ""
    sub = YouTubeTranscriptApi.get_transcript(video_id)
    for params in sub:
        # print(params['text'], end=' ')
        summary += params['text']
        summary += " "
    # print(summary)
    summarized_sub(summary)

# vid_id = input("Enter the YT video id(the part after the 'v='): ")
# show_transcripts(vid_id)

if __name__ == '__main__':
    app.run(debug = True)