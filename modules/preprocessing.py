# coding: utf-8


import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict

import read_from_csv
import write_to_csv
import exclude_keywords


def read_txt_data():

    # 読み込むcsvファイルの設定
    file_path = "../static/upload_file/test.txt"
    with open(file_path, encoding="utf-8_sig") as f:
        texts = f.read()
        print(texts)

    return texts


def read_exclude_words():  # 除外するワード
    # csvから情報取得
    file_path = "../csv/exclude_words.csv"
    columns = ["exclude_words"]
    ret_val = read_from_csv.run(file_path, columns)

    exclude_words = ret_val['exclude_words'].reset_index()['index'].tolist()
    return exclude_words




# 出てきた単語を記事ごとに保存
def write_words(_id, date, words, voc_arr, count_arr):
    file_path = '../csv/words.csv'
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


def create_array(_id, dates, articles):
    for i, article in enumerate(articles):
        words_count, words = counter(article)
        voc_arr = list(words_count.keys())
        count_arr = list(words_count.values())

        # csv書き出し
        # write_words(int(_id[i]), dates[i], words, voc_arr, count_arr)


def start():
    print("Preprocessing process start")
    # テキストの読み込み
    texts = read_txt_data()
    # 除外リストの読み込み
    # exclude_words = read_exclude_words()
    # リスト内の文字列を除外
    # articles = exclude_keywords.do_exclude(texts, exclude_words)
    # 単語に分解
    # create_array(ids, dates, articles)
    # ワードクラウド作成


if __name__ == "__main__":
    start()

