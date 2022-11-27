from gensim.models import Word2Vec
import warnings
warnings.filterwarnings('ignore')


class WordGensim:
    corpus = [['dog', 'bites', 'man'], ["man", "bites", "dog"],
              ["dog", "eats", "meat"], ["man", "eats", "food"]]

    model_cbow = Word2Vec(corpus, min_count=1, sg=0)
    print(model_cbow)
    print(model_cbow.wv['dog'])

    model_skipgram = Word2Vec(corpus, min_count=1, sg=1)
    print(model_skipgram)
    print(model_skipgram.wv['dog'])


if __name__ == '__main__':
    WordGensim()
