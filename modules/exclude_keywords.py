# 除外キーワードを元のデータから除外
def do_exclude(texts, exclude_words):
    print("Starting exclude specific keywords...")
    texts = texts.split(',')
    articles = []
    for article in texts:
        for exclude in exclude_words:
            article = article.replace(exclude, '')
        article.strip()
        articles.append(article)
    articles = ','.join(articles)
    return articles

if __name__ == "__main__":
  do_exclude()