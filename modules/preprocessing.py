# coding: utf-8

# ライブラリのインポート
import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict

# 自作APIの読み込み
from modules import read_from_csv
from modules import write_to_csv
from modules import exclude_keywords
from modules import word_cloud_generator


def read_txt_data():

    # 読み込むcsvファイルの設定
    file_path = "./static/upload_file/test.txt"
    with open(file_path, encoding="utf-8_sig") as f:
        texts = f.read()
        # print(texts)

    return texts


def read_exclude_words():  # 除外するワード
    # csvから情報取得
    file_path = "./csv/exclude_words.csv"
    columns = ["exclude_words"]
    ret_val = read_from_csv.run(file_path, columns)

    exclude_words = ret_val['exclude_words'].reset_index()['index'].tolist()
    return exclude_words


# 出てきた単語を記事ごとに保存
def write_words(_id, date, words, voc_arr, count_arr):
    file_path = './csv/words.csv'
    columns = ['id']
    written_words = read_from_csv.run(file_path, columns)

    storaged_article_id = written_words['id'].reset_index()['index'].tolist()

    if _id in storaged_article_id:
        print("This article has storaged(id: %d)" % _id)
    else:
        # 単語を記録
        columns = ['id', 'date', 'words']
        values = [_id, date, words]
        write_to_csv.write_data(file_path, columns, values)

        # 文字の登場回数を記録
        for i in range(len(voc_arr)):
            results = pd.DataFrame(
                [[_id, date, voc_arr[i],
                  count_arr[i]]],
                columns=['id', 'date', 'word', 'count']
            )
        # / ************************
        # wc = word_count
        # ************************ /
        wc_file_path = "../csv/words_count.csv"
        df = pd.read_csv(wc_file_path)
        df = pd.concat([df, results])
        df.to_csv(wc_file_path, index=False)
        print("success writing to %s" % wc_file_path)


def create_array(article):
    print("Starting explode to vocabulary...")
    _article = ""
    for i in article:
        _article += i

    t = Tokenizer()
    words_count = defaultdict(int)
    words = ""
    tokens = t.tokenize(_article)
    for token in tokens:
        pos = token.part_of_speech.split(',')[0]
        if pos == '名詞':
            # if pos == '名詞' or pos == '形容詞' or pos == '動詞':
            words_count[token.base_form] += 1
            words += token.base_form
            words += ","
    return words


def start():
    # importLibraries()
    print("Preprocessing process start")
    # テキストの読み込み
    texts = read_txt_data()
    # 除外リストの読み込み
    exclude_words = read_exclude_words()
    # 単語に分解
    _words = create_array(texts)
    # リスト内の文字列を除外
    words = exclude_keywords.do_exclude(_words, exclude_words)
    # ワードクラウド作成
    word_cloud_generator.genWordCloud(words)
    return "static/imgs/wordcloud.png"


if __name__ == "__main__":
    start()
