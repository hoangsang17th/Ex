
import codecs
from urllib.parse import urljoin
import logging
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
import requests
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from langdetect import detect
import underthesea

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:

    def __init__(self):
        self.visited_urls = []
        self.urls_to_visit = []
        self.number_of_article = 0
        self.filtered_words = []
        self.stop_words = []
        self.divider = "\n################ Hoàng Sang ##################\n"

    def create_text_file(self, soup):
        # Get text
        title = soup.find('h1', {'class': 'fs-headline1'})
        content = soup.find('div', {'class': 'js-post-body'})
        # Write text to file with encoding is utf-8
        file = codecs.open("D:\\E23.1\\NaturalLanguageProcessing\\Ex\\pipeline\\stackoverflow\\" +
                           str(self.number_of_article) + ". " +
                           str(soup.title.string
                               .replace("|", "").replace("(", "")
                               .replace("!", "").replace("/", "")
                               .replace("?", " (question mark)").replace(",", "")) + '.txt', "w", "utf-8")

        file.write(str(soup.title.string))

        file.write(self.divider)
        file.write("The text is written in the language: ")
        file.write(detect(soup.title.string))

        file.write(self.divider)
        sentence = "Phân từ cho văn bản tiếng Việt: (Bời vì truy vấn trong trang stackoverflow có khá ít nội dung tiếng việt nên em sử dụng một đoạn văn khác để thay thế)"
        file.write(sentence + "\n")
        file.write(str(underthesea.word_tokenize(sentence)))

        file.write(self.divider)
        file.write("This is the original text:\n")
        file.write(str(content.text) + "\n")

        #   split sentences with sent_tokenize
        file.write(self.divider)
        file.write("This is the text that has been Unicode Normalization: \n\n\n")
        for paragraph in sent_tokenize(content.text):
            #    Unicode Normalization with .encode("utf-8")
            file.write(str(paragraph.encode("utf-8")) + "\n")
            self.remove_stopwords(word_tokenize(paragraph))

        file.write(self.divider)
        file.write("Count and sorted stopWords: \n")
        file.write(str(self.count_stop_words()))

        file.write(self.divider)
        file.write("STEMMING: \n")
        for paragraph in sent_tokenize(content.text):
            for word in word_tokenize(paragraph):
                file.write(word + ": " + str(self.to_stemming(word)) + "\n")

        file.write(self.divider)
        file.write("LEMMATIZATION: \n")
        for paragraph in sent_tokenize(content.text):
            for word in word_tokenize(paragraph):
                file.write(word + ": " + str(self.to_lemmatizer(word)) + "\n")

        file.close()
        self.number_of_article += 1

    def to_lemmatizer(self, word):
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(word)

    def to_stemming(self, word):
        stemmer = PorterStemmer()
        return stemmer.stem(word)

    def remove_stopwords(self, wordTokenize):
        for word in wordTokenize:
            if word not in stopwords.words('english'):
                self.filtered_words.append(word)
            else:
                self.stop_words.append(word)

    def count_stop_words(self):
        count = {}
        for word in self.stop_words:
            count[word] = self.stop_words.count(word)
        sorted_count_words = {k: v for k, v in sorted(
            count.items(), key=lambda item: item[1], reverse=True)}
        return sorted_count_words

    def get_linked_urls(self, url, soup):
        for link in soup.find_all('a', {'class': 'question-hyperlink'}):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        self.create_text_file(soup)
        self.stop_words = []
        self.filtered_words = []
        for url in self.get_linked_urls(url, soup):
            self.add_url_to_visit(url)
        print("Link not visited: ", len(self.urls_to_visit))
        print("Link visited: ", len(self.visited_urls))

    def run(self):
        for num_page in range(0, 10):
            num_page = num_page + 1
            print("Page: ", num_page)
            page = requests.get(
                "https://stackoverflow.com/questions?tab=newest&pag" + str(num_page))
            soup = BeautifulSoup(page.content, 'html.parser')
            for url in self.get_linked_urls("https://stackoverflow.com/questions/", soup):
                self.add_url_to_visit(url)
        while (len(self.urls_to_visit) > 0 & self.number_of_article < 1000):
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)


if __name__ == '__main__':
    Crawler().run()
