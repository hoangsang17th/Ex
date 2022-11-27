
import re

import underthesea


class Main:
    def __init__(self):
        self.data = '<a herf="/iphone-14.html">Xem thông số kỹ thuật <b> iPhone 13</b>, cập nhập tháng 10 năm 2022 tại đây. Xin liên hệ để báo giá.</a>'

        self.TAG_RE = re.compile(r'<[^>]+>')

    def clean_html(self):
        self.htmlWithoutTag = re.sub(self.TAG_RE, '', self.data)
        print(self.htmlWithoutTag)

    def tokenize(self):
        self.tokenizeFinal = underthesea.word_tokenize(self.htmlWithoutTag)
        print(self.tokenizeFinal)

    def tokenize2(self):
        self.tokenizeFinal2 = underthesea.word_tokenize(self.htmlWithoutTag, format="text")
        print(self.tokenizeFinal2) 

    def run(self):
        self.clean_html()
        self.tokenize()
        self.tokenize2()


if __name__ == '__main__':
    Main().run()
