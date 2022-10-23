import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import json
import pickle

from underthesea import text_normalize, word_tokenize


class Training:
    def __init__(self):
        self.intents = json.loads(
            open('D:/E23.1/NaturalLanguageProcessing/Ex/final/data/intents.json', encoding='utf-8').read())
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_letters = ['?', '!', '.', ',']
        self.setup()

    def setup(self):
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                # Phân đoạn từ
                word_list = word_tokenize(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list, intent["tag"]))
                if intent["tag"] not in self.classes:
                    self.classes.append(intent["tag"])
        self.lemmatize()

    def lemmatize(self):
        self.words = sorted(list(set(self.words)))
        self.words = [text_normalize(word)
                      for word in self.words if word not in self.ignore_letters]

        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))
        pickle.dump(self.words, open(
            'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/words.pkl', 'wb'))
        pickle.dump(self.classes, open(
            'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/classes.pkl', 'wb'))
        self.train_data()

    def train_data(self):
        self.training = []
        self.output = [0] * len(self.classes)
        for document in self.documents:
            bag = []
            word_patterns = document[0]
            # Chuẩn hóa văn bản
            word_patterns = [text_normalize(
                word.lower())for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)
            output_row = list(self.output)
            output_row[self.classes.index(document[1])] = 1
            self.training.append([bag, output_row])

        train_x, train_y = self.returnContent()
        self.create_model(train_x, train_y)

    def returnContent(self):
        random.shuffle(self.training)
        self.training = np.array(self.training)
        train_x = list(self.training[:, 0])
        train_y = list(self.training[:, 1])
        print("Training data created")
        return train_x, train_y

    def create_model(self, train_x, train_y):
        model = Sequential()
        model.add(Dense(128, input_shape=(
            len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd, metrics=['accuracy'])

        model.fit(np.array(train_x), np.array(train_y),
                  epochs=200, batch_size=5, verbose=1)
        model.save(
            'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/chatbot_model.h5', model)
        print("model created")


if __name__ == '__main__':
    Training()
