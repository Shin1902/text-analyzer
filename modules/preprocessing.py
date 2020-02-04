# coding: utf-8

# ライブラリのインポート
import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict

# 自作APIの読み込み
from modules import read_from_csv
from modules import exclude_keywords
from modules import frequent_words
from modules import word_count
from modules import barchart
from modules import word_cloud_generator
from modules import cooccurence_network


def read_txt_data():

    # 読み込むファイルの設定
    file_path = "./static/upload_file/test.txt"
    with open(file_path, encoding="utf-8") as f:
        texts = f.read()
        # print(texts)
    f.close()
    return texts


def read_exclude_words():  # 除外するワード
    # csvから情報取得
    file_path = "./csv/exclude_words.csv"
    columns = ["exclude_words"]
    ret_val = read_from_csv.run(file_path, columns)

    exclude_words = ret_val['exclude_words'].reset_index()['index'].tolist()
    return exclude_words


def start():
    # importLibraries()
    print("Preprocessing process start")
    # テキストの読み込み
    texts = read_txt_data()
    # 除外リストの読み込み
    exclude_words = read_exclude_words()

    # **********************************************************
    #   文章の前処理
    # **********************************************************

    # 形態素解析
    words = frequent_words.run(texts)
    # リスト内の文字列を除外
    processed_words = exclude_keywords.do_exclude(words, exclude_words)

    # 頻出語句のカウント
    col_count = word_count.run(processed_words)
    bar = barchart.create_bar_chart(col_count)
    # ワードクラウド作成
    word_cloud_generator.genWordCloud(processed_words)

    #   共起ネットワークの作成
    cooccurence_network.run(texts, exclude_words)

    #   処理完了を知らせるための戻り値を返す
    return ["static/imgs/wordcloud.png", "static/imgs/cooc_net.png", bar]


if __name__ == "__main__":
    start()
