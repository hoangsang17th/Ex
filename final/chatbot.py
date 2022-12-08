import random
from flask import Flask, request
from googletrans import Translator
import numpy as np
from keras.models import load_model

import json
import pickle
from underthesea import text_normalize, word_tokenize

from langdetect import detect
# Lemmatize using WordNet's built-in morphy function.
# Returns the input word unchanged if it cannot be found in WordNet.

app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.form["message"]
    print(message)
    res = app.response_class(
        response=json.dumps({"message": Chatbot().chatbot_response(message)}),
        status=200,
        mimetype='application/json'
    )
    return res


class Chatbot:
    def __init__(self):
        # app = Flask(__name__)
        # socketio = SocketIO(app, cors_allowed_origins="*")
        #     socketio.run(app, host="localhost", port="3000")

        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.language = 'vi'

        self.path = 'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/'
        # Trích xuất dữ liệu đã được thu thập theo dạng utf-8
        self.intents = json.loads(
            open(self.path + 'intents.json', encoding='utf-8').read())
        # Tải dữ liệu từ các file đã được đào tạo trước đó
        self.words = pickle.load(open(self.path + 'words.pkl', 'rb'))
        self.classes = pickle.load(open(self.path + 'classes.pkl', 'rb'))
        self.model = load_model(self.path + 'model.h5')

        print("Chatbot is ready to talk!")

    def clean_up_sentence(self, sentence):
        # TODO: Thêm nhận dạng ngôn ngữ và sử dụng GG Translate API để dịch qua tiếng việt
        # Song ngữ rồi á
        try:
            self.language = detect(sentence)

        except:
            self.language = 'vi'
        if self.language != 'vi':
            translator = Translator(service_urls=['translate.googleapis.com'])
            sentence = translator.translate(sentence, dest='vi').text
            print("From: " + self.language + " To: " + 'vi')
            print("Translated:", sentence)
        # Phân đoạn từ
        sentence_words = word_tokenize(sentence)
        # Chuẩn hóa từ
        sentence_words = [text_normalize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        # Tạo một mảng với kích thước bằng số lượng từ trong từ điển
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, word in enumerate(self.words):
                if word == s:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        # Dự đoán thông qua mô hình đã được đào tạo và lấy về kết quả đầu tiên
        res = self.model.predict(np.array([bow]))[0]
        # Ngưỡng lỗi cho phép
        ERROR_THRESHOLD = 0.25
        # Lọc các kết quả có độ chính xác nhỏ hơn ngưỡng lỗi
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # Sắp xếp các kết quả theo độ chính xác
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []

        for r in results:
            return_list.append(
                {"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if (i['tag'] == tag):
                result = random.choice(i['responses'])
                break
        if self.language != 'vi':

            result = self.translator.translate(result, dest=self.language).text
        return result

    def chatbot_response(self, msg):
        ints = self.predict_class(msg)
        return self.get_response(ints, self.intents)

    def run(self):
        while True:
            message = str(input('You: '))
            res = self.chatbot_response(message)
            print("BOT: " + res)


if __name__ == '__main__':

    # app.run(host="127.0.0.1", port=3000, debug=True)
    Chatbot().run()
