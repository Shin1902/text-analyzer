import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def read_words():
    csv_file = "../csv/words.csv"
    df = pd.read_csv(csv_file)

    _id = df['id']
    date = df['date']
    words = df['words']
    return _id, date, words



def genWordCloud():

  _id, date, words = read_words()

  # print(words)


  texts = ' '.join(words)
  fpath = "../font/NotoSansCJKjp-Regular.otf"
  wordcloud = WordCloud(font_path=fpath, width=480, height=320)

  print("Generating wordcloud...")
  wordcloud.generate(texts)
  wordcloud.to_file('../img/wordcloud.png')
  print("Successfully generate wordcloud png image!")

if __name__ == '__main__':
  genWordCloud()