import random
from flask_socketio import SocketIO
import numpy as np
from keras.models import load_model

import json
import pickle
from flask import Flask, render_template, request
from underthesea import text_normalize, word_tokenize
# Lemmatize using WordNet's built-in morphy function.
# Returns the input word unchanged if it cannot be found in WordNet.
app = Flask(__name__)

intents = json.loads(
    open('D:/E23.1/NaturalLanguageProcessing/Ex/final/data/intents.json', encoding='utf-8').read())
words = pickle.load(
    open("D:/E23.1/NaturalLanguageProcessing/Ex/final/data/words.pkl", 'rb'))
classes = pickle.load(
    open("D:/E23.1/NaturalLanguageProcessing/Ex/final/data/classes.pkl", 'rb'))
model = load_model(
    'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/chatbot_model.h5')

print("Chatbot is ready to talk! Type 'quit' to exit")

socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    if msg == 'quit':
        print('Chatbot is offline')
        return
    res = chatbot_response(msg)
    socketio.emit('message', res)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.form["message"]
    print(message)
    res = app.response_class(
        response=json.dumps({"message": chatbot_response(message)}),
        status=200,
        mimetype='application/json'
    )
    return res


def chatbot_response(msg):
    ints = predict_class(msg)
    return getResponse(ints, intents)


def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence)
    sentence_words = [text_normalize(
        word) for word in sentence_words]
    return sentence_words


def bow(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    p = bow(sentence)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append(
            {"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


if __name__ == '__main__':
    socketio.run(app, host="192.168.1.7", port="3000")
