# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np


# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "TEA | Text Analyzer"
    con_title = "テキスト解析"
    message = "テキストファイル(.txt)を選択してください。"

    # index.html をレンダリングする
    return render_template('index.html', message=message, title=title, con_title=con_title)


@app.route('/upload_file', methods=['GET', 'POST'])
def post():
    title = "TEA | Text Analyzer"
    con_title = "テキスト解析"

    if request.method == 'POST':
        _file = request.files.get('uploading_file')
        filename = secure_filename(_file.filename)

        if filename == "":
            print("/ *********************************************************")
            print("Nothing was uploaded")
            print("********************************************************* /")
            message = "ファイルを指定してください。"
            return render_template('index.html', title=title, con_title=con_title, message=message)
        else:
            print("/ *********************************************************")
            print("Uploaded file name: " + filename)
            print("********************************************************* /")

            # ファイルの一時保存
            _file.save('./static/upload_file/' + filename)
            message = "アップロードが完了しました。"
            return render_template('index.html', title=title, con_title=con_title, message=message)




if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
