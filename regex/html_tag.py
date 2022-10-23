import re


class RemoveHtmlTag:
    # Define Regex
    def __init__(self):
        self.TAG_RE = re.compile(r'<[^>]+>')

    def clean_html(self, raw_html):

        cleantext = re.sub(self.TAG_RE, '', raw_html)
        print(cleantext)


if __name__ == '__main__':
    html = """<!DOCTYPE html >
                    <html >
                    <head >
                        <title > Page Title < /title >
                    </head >
                    <body >

                        <h1 > This is a Heading < /h1 >
                        <p > This is a paragraph. < /p >

                    </body >
                    </html >"""
    RemoveHtmlTag().clean_html(html)
