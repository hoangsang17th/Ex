
import codecs
from urllib.parse import urljoin
import logging
from bs4 import BeautifulSoup
import requests


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:

    def __init__(self):
        self.visited_urls = []
        self.urls_to_visit = []
        self.number_of_article = 0

    def create_text_file(self, soup):
        # Get text
        title = soup.find('h1', {'class': 'css-4kh4rf'})
        content = soup.find('div', {'class': 'css-1wr68sm'})
        # Write text to file with encoding is utf-8
        file = codecs.open("D:\\E23.1\\NaturalLanguageProcessing\\Ex\\crawl\\phongvu\\" +
                           str(self.number_of_article) + ". " +
                           str(soup.title.string
                               .replace("|", "").replace("(", "")
                               .replace(")", "").replace("/", "")
                               .replace("\"", "Inch").replace(",", "")) + '.txt', "w", "utf-8")
        #    Unicode Normalization with .encode("utf-8")
        #    Replace dot with \n for line break
        #   Remove .encode("utf-8") to see the text in readable form
        file.write(str(content.text).replace(
            ". ", "\n").replace("? ", "\n") + "\n")
        file.close()
        self.number_of_article += 1

    def get_linked_urls(self, url, soup):
        for link in soup.find_all('a', {'class': 'css-1um6yby'}):
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
        for url in self.get_linked_urls(url, soup):
            self.add_url_to_visit(url)
        print("Link not visited: ", len(self.urls_to_visit))
        print("Link visited: ", len(self.visited_urls))

    def run(self):
        for num_page in range(0, 6):
            num_page = num_page + 1
            print("Page: ", num_page)
            page = requests.get(
                "https://phongvu.vn/acer-brand.acer?brandId=acer&page=" + str(num_page))
            soup = BeautifulSoup(page.content, 'html.parser')
            for url in self.get_linked_urls("https://phongvu.vn/", soup):
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
