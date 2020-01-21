# coding: utf-8

from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as font_manager
from copy import copy, deepcopy
from collections import defaultdict, Counter
import MeCab
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.rcParams['font.family'] = 'Yu Gothic'
np.random.seed(0)


# MeCabの準備
mecab = MeCab.Tagger()
mecab.parse('')


# テキストデータの取得
def read_txt_data():
    csv = "../csv/txt_data.csv"
    df = pd.read_csv(csv)

    ids = df['id']
    dates = df['date']
    texts = df['text']

    return ids, dates, texts


def read_exclude_words():  # 除外するワード
    csv = "../csv/exclude_words.csv"
    df = pd.read_csv(csv)

    exclude_words = df['exclude_words'].reset_index()['index'].tolist()
    return exclude_words


# 10行記事ごとに読み込み、名詞と頻度を抽出


def pick_keywords(texts, exclude_words):
    # 文章の読み込みとNode, Edgeの切りだし
    node_name = defaultdict(str)
    node_idx = defaultdict(int)
    node_type = defaultdict(list)
    node_count = defaultdict(int)
    edge_list = []

    cnt = 0
    for line in list(texts):
        node = mecab.parseToNode(line)
        node_prev = None
        while node:
            w = node.surface
            w_type = node.feature.split(',')[0]
            if (w_type in ["名詞"]) & (w not in exclude_words):
                # Nodeの処理
                if w not in node_name.values():
                    node_name[cnt] = w
                    node_idx[w] = cnt
                    node_count[cnt] = 1
                    node_type[w_type].append(node_idx[w])
                    cnt += 1
                else:
                    node_count[node_idx[w]] += 1
                # edgeの処理
                # 循環グラフを回避
                if (node_prev is not None) & (node_prev != node_idx[w]):
                    # 有向グラフを回避
                    edge = (min(node_prev, node_idx[w]), max(
                        node_prev, node_idx[w]))
                    edge_list.append(edge)
                node_prev = node_idx[w]
            node = node.next
            if node is None:
                break

    edge_count = Counter(edge_list)

    return node_name, node_type, node_count, edge_list, edge_count


def gen_network(node_name, node_type, node_count, edge_list, edge_count, date):
    # Networkxに格納
    G = nx.Graph()
    G.add_nodes_from([(idx, {'cnt': node_count[idx]}) for idx in node_name])
    G.number_of_nodes(), len(node_name)
    G.add_edges_from([(a, b, {'cnt': edge_count[(a, b)]})
                      for a, b in edge_list])

    # Node, Edgeを剪定
    G2 = deepcopy(G)
    # Node: cnt >= 3で剪定
    # 破壊的操作なので、予め破壊用のグラフ(G2)と検索用グラフ(G)を分けておく
    for n, attr in G.nodes().items():
        if (attr['cnt'] < 30):
            G2.remove_edges_from(list(G.edges(n)))
            G2.remove_node(n)

    G3 = deepcopy(G2)
    # Edge: cnt >= 2で剪定
    # Edgeが無くなったNodeは、一旦そのまま
    for e, attr in G2.edges().items():
        if attr['cnt'] < 30:
            G3.remove_edge(*e)

    G4 = deepcopy(G3)
    # Edgeが無くなったNodeを削除
    for n in list(G3.nodes()):
        if len(G3[n]) == 0:
            G4.remove_node(n)

    G_result = deepcopy(G4)  # 描画に使う剪定後のグラフを確定

    # pos = nx.layout.spring_layout(G_result, k=0.7, seed=10) # 2次元平面状の座標を計算
    pos = nx.layout.spring_layout(G_result, k=0.7)  # 2次元平面状の座標を計算
    labels = {n: node_name[n] for n in pos.keys()}  # Nodeに日本語を描画するための辞書
    # node_size = [np.log(node_count[n])*400 for n in pos.keys()] # 対数スケール
    node_size = [node_count[n]*10 for n in pos.keys()]

    edge_alpha = [edge_count[e] for e in G_result.edges()]
    edge_colors = [edge_count[e] for e in G_result.edges()]
    edge_width = [edge_count[e] * 0.08 for e in G_result.edges()]

    # 描画
    fig, ax = plt.subplots(figsize=(12, 12))
    # 名詞のNodeを描画
    # Nodeを色分けしたいときは、nodelistを使ってNodeのグループ毎に描画関数を繰り返し実行する
    # nodelistはグループ毎のNode番号を指定するが、それ以外の引数(posやnode_sizeなど)は全てのNodeについての値を入れる
    # 指定出来る色はmatplotlibのcolor exampleを参照
    # https://matplotlib.org/examples/color/named_colors.html
    nx.draw_networkx_nodes(G_result, pos,
                           nodelist=[n for n in G_result.nodes()
                                     if n in node_type["名詞"]],
                           node_size=node_size, node_color="#f0f0f0", alpha=0.6, ax=ax)
    # nx.draw_networkx_nodes(G_result, pos,
    #                        nodelist=[n for n in G_result.nodes()
    #                                  if n in node_type["動詞"]],
    #                        node_size=node_size, node_color="yellowgreen", alpha=0.6, ax=ax)
    # nx.draw_networkx_nodes(G_result, pos,
    #                        nodelist=[n for n in G_result.nodes()
    #                                  if n in node_type["形容詞"]],
    #                        node_size=node_size, node_color="tomato", alpha=0.6, ax=ax)

    # edgeの色に濃淡をつけたいときは、edge_colorに数値のlistを代入してedge_cmapを使用
    # Sequentialなカラーマップから好きなやつを選ぶ
    # https://matplotlib.org/examples/color/colormaps_reference.html
    # 色の濃淡の具合はedge_vmin, edge_vmaxで調整
    nx.draw_networkx_edges(G_result, pos, alpha=0.6,
                           width=edge_width, edge_color=edge_colors,
                           edge_vmin=0, edge_vmax=20,
                           edge_cmap=plt.cm.Blues, ax=ax)
    # Nodeにラベルをつけたいときは、以下の関数を使う
    # font_familyにPCに入っている日本語フォントを指定してあげると、日本語を描画してくれる
    nx.draw_networkx_labels(G_result, pos, labels, font_size=12,
                            font_family="Yu Gothic", ax=ax)


    plt.savefig("./img/%s.png" % date)
    # plt.show()


def start():

    exclude_words = read_exclude_words()
    ids, dates, texts = read_txt_data()

    # for i, txt in enumerate(texts):
    #     # print("****")
    #     # print(txt)
    #     # print("<br />")
    #     node_name, node_type, node_count, edge_list, edge_count = pick_keywords(
    #         txt, exclude_words)
    #     gen_network(node_name, node_type, node_count,
    #                 edge_list, edge_count, dates[i])

    node_name, node_type, node_count, edge_list, edge_count = pick_keywords(
        texts, exclude_words)

    gen_network(node_name, node_type, node_count,
                edge_list, edge_count, "test")


start()
