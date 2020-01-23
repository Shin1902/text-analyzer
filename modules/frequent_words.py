import MeCab
m = MeCab.Tagger('-Ochasen')


def read_text():
    filename = "../static/upload_file/test.txt"
    with open(filename, encoding="utf-8_sig") as f:
        text = f.read()

    f.close()
    return text


def parse_text(text):
    node = m.parseToNode(text)
    words = []
    while node:
        # pos = part of speech = 品詞
        pos = node.feature.split(",")[0]
        if pos in ["名詞", "動詞", "形容詞"]:
            # ************************************
            # node.feature
            #   0番目: 単語の品詞情報
            #   6番目: 原型データ
            # *************************************
            origin = node.feature.split(",")[6]
            words.append(origin)
        node = node.next
    return words


def start():
    text = read_text()
    words = parse_text(text)


def run(text):
    words = parse_text(text)
    return words


if __name__ == "__main__":
    start()
