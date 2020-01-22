def run(target_file):
    with open('./static/upload_file/' + target_file, encoding="utf-8_sig") as f:
        text_contents = f.read()
        return text_contents
