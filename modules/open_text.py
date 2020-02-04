def run(target_file):
    with open('./static/upload_file/' + target_file, encoding="utf-8") as f:
        text_contents = f.read()
        return text_contents
