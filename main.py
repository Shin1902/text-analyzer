# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import numpy as np

from modules import preprocessing
from modules import open_text
from modules import barchart

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.secret_key = "jvodmv;eofg52f5b1d8h6d2d78gh5h8r"


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "TEA | Text Analyzer"
    con_title = "ようこそ"
    message = "左のメニューから利用したい機能を選択してください。"

    if 'target_file' in session:
        target_file = session['target_file']
        text_contents = open_text.run(target_file)
        return render_template('index.html', title=title, con_title=con_title, message=message, target_file=target_file, text_contents=text_contents)
    else:
        return render_template('index.html', message=message, title=title, con_title=con_title)


# /* --------------------------------------------------------------
#   ワードクラウド
# -------------------------------------------------------------- */

@app.route('/word_cloud')
def word_cloud_page():
    title = "TEA | WordCloudの作成"
    con_title = "ワードクラウド"
    message = "出現頻度の高いキーワードを強調して表示しています。"

    if 'target_file' in session:
        target_file = session['target_file']
        wc_img_path = session['wc_img_path']
        return render_template('word_cloud.html', message=message, title=title, con_title=con_title, target_file=target_file, wc_img_path=wc_img_path)
    else:
        return render_template('word_cloud.html', message=message, title=title, con_title=con_title)



# /* --------------------------------------------------------------
#   共起ネットワーク
# -------------------------------------------------------------- */

@app.route('/cooc_net')
def cooc_net_page():
    title = "TEA | 共起ネットワークの作成"
    con_title = "共起ネットワーク"
    message = "関連するキーワード同士を結んだネットワークです。"

    if 'target_file' in session:
        target_file = session['target_file']
        co_img_path = session['co_img_path']
        return render_template('cooc_net.html', message=message, title=title, con_title=con_title, target_file=target_file, co_img_path=co_img_path)
    else:
        return render_template('cooc_net.html', message=message, title=title, con_title=con_title)

# /* --------------------------------------------------------------
#   頻出度
# -------------------------------------------------------------- */

@app.route('/frequent_words')
def frequent_words():
    title = "TEA | 頻出語句のグラフ表示"
    con_title = "頻出語句のグラフ表示"
    message = "アップロードしたテキストデータ内の頻出語句をグラフ化したものです。"

    if 'target_file' in session:
        target_file = session['target_file']
        with open('./static/settings/graph_data.txt') as f:
            bar = f.read()

        return render_template('frequent_words.html', message=message, title=title, con_title=con_title, target_file=target_file, plot=bar)
    else:
        return render_template('frequent_words.html', message=message, title=title, con_title=con_title)



@app.route('/upload_file', methods=['GET', 'POST'])
def post():
    title = "TEA | Text Analyzer"
    con_title = "ようこそ"

    if request.method == 'POST':
        # *****************************************
        #   アップロードされたファイルを確認
        # *****************************************
        _file = request.files.get('uploading_file')
        filename = secure_filename(_file.filename)
        session['target_file'] = filename  # セッションに登録

        if filename == "":
            print("/ ---------------------------------------------------------")
            print("Nothing was uploaded")
            print("--------------------------------------------------------- /")
            message = "ファイルを指定してください。"
            return render_template('index.html', title=title, con_title=con_title, message=message)
        else:
            print("/ ---------------------------------------------------------")
            print("Uploaded file name: " + filename)
            print("--------------------------------------------------------- /")

            # ファイルの一時保存
            _file.save('./static/upload_file/' + filename)
            message = "アップロードが完了しました。"
            
            # *****************************************
            #   ワードクラウドを作成
            # *****************************************
            result_process = preprocessing.start()
            url = url_for("index", _external=True)
            wc_path = url + result_process[0]
            co_path = url + result_process[1]

            session['wc_img_path'] = wc_path
            session['co_img_path'] = co_path

            # グラフ用のデータを保存
            with open('./static/settings/graph_data.txt', mode='w') as f:
                f.write(result_process[2])


            target_file = filename
            text_contents = open_text.run(target_file)
            return redirect("/")


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
