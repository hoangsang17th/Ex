from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDF:
    def __init__(self):
        self.documents = ""

    def run(self):
        self.getData()
        self. buildTheVocabulary()
        self.getTDIDF()

    def getData(self):
        file = open(
            "D:/E23.1/NaturalLanguageProcessing/Ex/crawl/phongvu/9. Màn hình LCD Acer 21.5Inch R221QB.txt", "r", encoding="utf8")
        self.documents = file.read()
        self.processed_docs = self.documents.replace(
            ".", " ").replace(",", " ").replace("-", " ").lower().split()

    def buildTheVocabulary(self):
        self.tfidf = TfidfVectorizer()
        self.bow_rep_tfidf = self.tfidf.fit_transform(self.processed_docs)
        # IDF for all words in the vocabulary
        print("IDF for all words in the vocabulary", self.tfidf.idf_)
        print("-"*10)
        # All words in the vocabulary.
        print("All words in the vocabulary", self.tfidf.get_feature_names())
        print("-"*10)
        # TFIDF representation for all documents in our corpus
        print("TFIDF representation for all documents in our corpus\n",
              self.bow_rep_tfidf.toarray())
        print("-"*10)

    def getTDIDF(self):
        self.temp = self.tfidf.transform(["THIẾT KẾ SANG TRỌNG".lower()])
        print("Tfidf representation for 'THIẾT KẾ SANG TRỌNG':\n",
              self.temp.toarray())


if __name__ == '__main__':
    TFIDF().run()
