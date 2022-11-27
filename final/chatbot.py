import random
from googletrans import Translator
import numpy as np
from keras.models import load_model

import json
import pickle
from underthesea import text_normalize, word_tokenize

from langdetect import detect
# Lemmatize using WordNet's built-in morphy function.
# Returns the input word unchanged if it cannot be found in WordNet.
# app = Flask(__name__)

path = 'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/'
# Trích xuất dữ liệu đã được thu thập theo dạng utf-8
intents = json.loads(open(path + 'intents.json', encoding='utf-8').read())
# Tải dữ liệu từ các file đã được đào tạo trước đó
words = pickle.load(open(path + 'words.pkl', 'rb'))
classes = pickle.load(open(path + 'classes.pkl', 'rb'))
model = load_model(path + 'model.h5')

print("Chatbot is ready to talk!")

# socketio = SocketIO(app, cors_allowed_origins="*")


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/chatbot', methods=['POST'])
# def chatbot():
#     message = request.form["message"]
#     print(message)
#     res = app.response_class(
#         response=json.dumps({"message": chatbot_response(message)}),
#         status=200,
#         mimetype='application/json'
#     )
#     return res


def clean_up_sentence(sentence):
    # TODO: Thêm nhận dạng ngôn ngữ và sử dụng GG Translate API để dịch qua tiếng việt
    # Song ngữ rồi á
    language = detect(sentence)
    if language != 'vi':
        translator = Translator(service_urls=['translate.googleapis.com'])
        sentence = translator.translate(sentence, dest='vi').text
        print("Translated: ", sentence)
    # Phân đoạn từ
    sentence_words = word_tokenize(sentence)
    # Chuẩn hóa từ
    sentence_words = [text_normalize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    # Tạo một mảng với kích thước bằng số lượng từ trong từ điển
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    # Dự đoán thông qua mô hình đã được đào tạo và lấy về kết quả đầu tiên
    res = model.predict(np.array([bow]))[0]
    # Ngưỡng lỗi cho phép
    ERROR_THRESHOLD = 0.25
    # Lọc các kết quả có độ chính xác nhỏ hơn ngưỡng lỗi
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Sắp xếp các kết quả theo độ chính xác
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append(
            {"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg)
    return get_response(ints, intents)


while True:
    message = input('You: ')

    ints = predict_class(message)
    res = get_response(ints, intents)
    print("BOT: " + res)

# if __name__ == '__main__':
#     socketio.run(app, host="localhost", port="3000")
