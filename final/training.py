import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import json
import pickle

from underthesea import text_normalize, word_tokenize
import matplotlib.pyplot as plt


class Training:
    def __init__(self):
        # Trích xuất dữ liệu đã được thu thập theo dạng utf-8
        self.path = 'D:/E23.1/NaturalLanguageProcessing/Ex/final/data/'
        self.intents = json.loads(
            open(self.path + 'intents.json', encoding='utf-8').read())
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
                # Thêm các cụm từ vào danh sách từ
                self.words.extend(word_list)
                # Thêm các cụm từ và nhãn vào danh sách tài liệu
                self.documents.append((word_list, intent["tag"]))
                if intent["tag"] not in self.classes:
                    self.classes.append(intent["tag"])

        print("Setup completed")
        self.lemmatizer()

    def lemmatizer(self):
        print("Lemmatizing...")
        # Chuẩn hóa văn bản và loại bỏ các ký tự đặc biệt
        self.words = [text_normalize(
            word) for word in self.words if word not in self.ignore_letters]
        print("Lemmatizer completed")
        # Sắp xếp các từ theo thứ tự bảng chữ cái
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))
        # Lưu các từ và nhãn vào file với pickle
        pickle.dump(self.words, open(self.path + 'words.pkl', 'wb'))
        pickle.dump(self.classes, open(self.path + 'classes.pkl', 'wb'))
        self.train_data()

    def train_data(self):
        print("Training data...")
        self.training = []
        # Tạo một mảng 0 với kích thước bằng số lượng nhãn
        self.output = [0] * len(self.classes)
        # One-hot encoding
        for document in self.documents:
            bag = []
            word_patterns = document[0]
            # Chuẩn hóa văn bản
            # các từ được chuyển thành chữ thường
            word_patterns = [text_normalize(word.lower())
                             for word in word_patterns]
            for word in self.words:
                # Nếu từ xuất hiện trong cụm từ thì gán giá trị 1
                bag.append(1) if word in word_patterns else bag.append(0)
            output_row = list(self.output)
            output_row[self.classes.index(document[1])] = 1
            self.training.append([bag, output_row])
        # training sẽ là tập hợp các cặp one-hot encoding và nhãn
        print("Training data completed")
        train_x, train_y = self.shuffleVectors()
        self.create_model(train_x, train_y)

    def shuffleVectors(self):
        # Trộn các cặp one-hot encoding và nhãn
        random.shuffle(self.training)
        self.training = np.array(self.training, dtype=object)
        # Tách tập huấn luyện thành 2 phần
        # train_x là tập các cặp one-hot encoding
        train_x = list(self.training[:, 0])
        # train_y là tập các nhãn
        train_y = list(self.training[:, 1])
        return train_x, train_y

    def create_model(self, train_x, train_y):
        print("Creating model...")
        # Khởi tạo mô hình Sequential (Tuần tự)
        model = Sequential()
        # Thêm lớp Dense với 128 đầu ra và hàm kích hoạt là relu
        model.add(Dense(128, input_shape=(
            len(train_x[0]),), activation='relu'))
        # Thêm lớp Dropout với tỉ lệ bỏ 0.5
        model.add(Dropout(0.5))
        # Thêm lớp Dense với 64 đầu ra và hàm kích hoạt là relu
        model.add(Dense(64, activation='relu'))
        # Thêm lớp Dropout với tỉ lệ bỏ 0.5
        model.add(Dropout(0.5))
        # Thêm lớp Dense với số đầu ra bằng số lượng nhãn và hàm kích hoạt là softmax
        model.add(Dense(len(train_y[0]), activation='softmax'))
        # Compile mô hình với hàm mất mát là categorical_crossentropy
        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd, metrics=['accuracy'])
        # Huấn luyện mô hình với tập huấn luyện
        # epochs là số lần lặp lại quá trình huấn luyện
        # batch_size là số lượng mẫu huấn luyện trong mỗi lần lặp
        # verbose là kiểu hiển thị quá trình huấn luyện => 0 là không hiển thị, 1 là hiển thị
        # Đầu vào là tập huấn luyện và đầu ra là tập nhãn
        history = model.fit(np.array(train_x), np.array(train_y),
                            epochs=200, batch_size=5, verbose=0, validation_data=(np.array(train_x), np.array(train_y)))
        # Lưu mô hình vào file
        model.save(self.path + 'model.h5', history)
        print("Model created")

        self.plot_model_history(history)

# Tiếp theo ta plot các thông số loss và acc ra

    def plot_model_history(self, model_history):
        acc = 'accuracy'
        val_acc = 'val_accuracy'
        loss = 'loss'
        val_loss = 'val_loss'
        print("Plotting model history...")
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))
        # # summarize history for accuracy
        axs[0].plot(range(1, len(model_history.history[acc]) + 1),
                    model_history.history[acc])
        axs[0].plot(range(1, len(model_history.history[val_acc]) + 1),
                    model_history.history[val_acc])
        axs[0].set_title('Model Accuracy')
        axs[0].set_ylabel('Accuracy')
        axs[0].set_xlabel('Epoch')
        # axs.set_xticks(np.arange(1, len(model_history.history[acc]) + 1),
        #                   len(model_history.history[acc]) / 10)
        axs[0].legend(['train', 'val'], loc='best')
        # summarize history for loss
        axs[1].plot(range(1, len(model_history.history[loss]) + 1),
                    model_history.history[loss])
        axs[1].plot(range(1, len(model_history.history[val_loss]) + 1),
                    model_history.history[val_loss])
        axs[1].set_title('Model Loss')
        axs[1].set_ylabel('Loss')
        axs[1].set_xlabel('Epoch')
        # axs[1].set_xticks(np.arange(1, len(model_history.history['loss']) + 1),
        #                   len(model_history.history['loss']) / 10)
        axs[1].legend(['train', 'val'], loc='best')
        fig.savefig(self.path + 'train.png')
        plt.show()


if __name__ == '__main__':
    Training()
