from gensim.models import Word2Vec
import warnings
warnings.filterwarnings('ignore')


class WordGensim:
    corpus = [['dog', 'bites', 'man'], ["man", "bites", "dog"],
              ["dog", "eats", "meat"], ["man", "eats", "food"]]

    # Training the model
    # using CBOW Architecture for trainnig
    model_cbow = Word2Vec(corpus, min_count=1, sg=0)
    # using skipGram Architecture for training
    model_skipgram = Word2Vec(corpus, min_count=1, sg=1)

    # Summarize the loaded model
    print(model_cbow)

    # Summarize vocabulary
    words = list(model_cbow.wv.vocab)
    print(words)

    # Acess vector for one word
    print(model_cbow['dog'])


if __name__ == '__main__':
    WordGensim()
