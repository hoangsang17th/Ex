from sklearn.feature_extraction.text import CountVectorizer


class BagOfNGrams:
    def __init__(self):
        self.documents = ""

    def run(self):
        self.getData()
        self. buildTheVocabulary()
        print(self.getBagOfNGrams(20))

    def getData(self):
        file = open(
            "D:/E23.1/NaturalLanguageProcessing/Ex/crawl/phongvu/9. Màn hình LCD Acer 21.5Inch R221QB.txt", "r", encoding="utf8")
        self.documents = file.read()
        self.processed_docs = self.documents.replace(
            ".", " ").replace(",", " ").replace("-", " ").lower().split()

    def buildTheVocabulary(self):
        self.count_vect = CountVectorizer(ngram_range=(1, 3))
        # Build a BOW representation for the corpus
        self.bow_rep = self.count_vect.fit_transform(self.processed_docs)

        # Look at the vocabulary mapping
        print("Our vocabulary: ", self.count_vect.vocabulary_)

    def getBagOfNGrams(self, position):
        return self.bow_rep[position].toarray()


if __name__ == '__main__':
    BagOfNGrams().run()
