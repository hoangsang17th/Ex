from gensim.models import Word2Vec


class Main:
    def __init__(self):
        self.documents1 = 'He wants to become a great inventor.'
        self.documents2 = 'She wants to become a famous person'

    def run(self):
        # Ex 1
        print("One hot vector:")
        self.buildTheVocabulary()
        print(self.getOnehotVector("great"))

        print("Word Embeddings:")
        print(self.wordEmbeddings())

    def buildTheVocabulary(self):
        self.vocab = {}
        self.count = 0
        for word in self.documents1.split():
            if word not in self.vocab:
                self.count = self.count + 1
                self.vocab[word] = self.count

    def getOnehotVector(self, somestring):
        onehot_encoded = []
        for word in somestring.split():
            temp = [0]*len(self.vocab)
            if word in self.vocab:
                # -1 is to take care of the fact indexing in array starts from 0 and not 1
                temp[self.vocab[word]-1] = 1
            onehot_encoded.append(temp)
        return onehot_encoded

    def wordEmbeddings(self):
        self.corpus = [self.documents1.split(" "), self.documents2.split(" ")]

        # Training the model
        # using CBOW Architecture for trainnig
        self.model_cbow = Word2Vec(self.corpus, min_count=1, sg=0)
        return self.model_cbow


if __name__ == '__main__':
    Main().run()
