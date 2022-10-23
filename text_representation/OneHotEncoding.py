class OneHotEncoding:
    def __init__(self):
        self.documents = ""

    def run(self):
        self.getData()
        self. buildTheVocabulary()
        print(self.getOnehotVector("Mô TIẾT".lower()))

    def getData(self):
        file = open(
            "D:/E23.1/NaturalLanguageProcessing/Ex/crawl/phongvu/9. Màn hình LCD Acer 21.5Inch R221QB.txt", "r", encoding="utf8")
        self.documents = file.read()
        self.processed_docs = self.documents.replace(
            ".", " ").replace(",", " ").replace("-", " ").lower()

    def buildTheVocabulary(self):
        self.vocab = {}
        self.count = 0
        for word in self.processed_docs.split():
            if word not in self.vocab:
                self.count = self.count + 1
                self.vocab[word] = self.count

    # Get one hot representation for any string based on this vocabulary.
    # If the word exists in the vocabulary, its representation is returned.
    # If not, a list of zeroes is returned for that word.
    def getOnehotVector(self, somestring):
        onehot_encoded = []
        for word in somestring.split():
            temp = [0]*len(self.vocab)
            if word in self.vocab:
                # -1 is to take care of the fact indexing in array starts from 0 and not 1
                temp[self.vocab[word]-1] = 1
            onehot_encoded.append(temp)
        return onehot_encoded


if __name__ == '__main__':
    OneHotEncoding().run()
