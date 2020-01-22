import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt



def genWordCloud(words):

  fpath = "./font/NotoSansCJKjp-Regular.otf"
  wordcloud = WordCloud(font_path=fpath, width=480, height=320)

  print("Generating wordcloud...")
  wordcloud.generate(words)
  # wordcloud.to_file('./img/wordcloud.png')
  wordcloud.to_file('./static/imgs/wordcloud.png')
  print("Successfully generate wordcloud png image!")

if __name__ == '__main__':
  genWordCloud()