import json
from googletrans import Translator
import translators as ts


class Translate():
    def __init__(self):
        self.text = ""
        self.filename = "D:/E23.1/NaturalLanguageProcessing/Ex/translate/dataset.json"

        self.translator = Translator(service_urls=['translate.googleapis.com'])

        self.dataset = json.loads(
            open(self.filename, "r", encoding='utf-8').read())
        self.dataFinal = json.loads(
            open(self.filename, "r", encoding='utf-8').read())

        # self.getBingTranslator()
        print(self.LD("Python", "pitrterretthon"))

    def setupGGTranslator(self):
        for data in self.dataset["Default"]:
            print(data["ID"])
            tempJson = json.dumps(data)
            currentJson = json.loads(tempJson)
            self.text = self.translator.translate(
                data["A"], dest='vi', src="en").text
            self.dataFinal["Default"].remove(currentJson)
            currentJson.update({"GV": self.text})
            self.dataFinal["Default"].append(currentJson)
        json.dump(self.dataFinal,
                  open(self.filename, "w", encoding='utf-8'), ensure_ascii=False)

    # Cái này chạy 2 lần thì mới chạy được
    # API bị giới hạn ở 60 lần
    def getBingTranslator(self):
        for i in range(0, 50):
            data = self.dataset["Default"][i]
            print(data["ID"])
            tempJson = json.dumps(data)
            currentJson = json.loads(tempJson)
            self.text = ts.bing(data["A"], from_language='en',
                                to_language='vi', if_use_cn_host=False)
            self.dataFinal["Default"].remove(currentJson)
            currentJson.update({"BV": self.text})
            self.dataFinal["Default"].append(currentJson)
        json.dump(self.dataFinal,
                  open(self.filename, "w", encoding='utf-8'), ensure_ascii=False)

    def LD(self, s, t):
        if s == "":
            return len(t)
        if t == "":
            return len(s)
        if s[-1] == t[-1]:
            cost = 0
        else:
            cost = 1

        res = min([self.LD(s[:-1], t)+1,
                   self.LD(s, t[:-1])+1,
                   self.LD(s[:-1], t[:-1]) + cost])

        return res


if __name__ == '__main__':
    Translate()
