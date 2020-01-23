import collections


def run(words):
    words = words.split(',')
    col_count = collections.Counter(words)
    # print(col_count.most_common(10))
    # print(type(col_count))
    return col_count