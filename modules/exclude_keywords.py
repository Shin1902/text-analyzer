# 除外キーワードを元のデータから除外
def do_exclude(texts, exclude_words):
    print("Starting exclude specific keywords...")
    articles = []
    for article in texts:
        for exclude in exclude_words:
            article = article.replace(exclude, '')
        article.strip()
        articles.append(article)
    return articles

if __name__ == "__main__":
  do_exclude()