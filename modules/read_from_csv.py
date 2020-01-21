import pandas as pd


def run(file_path, columns):
    df = pd.read_csv(file_path)

    return_value = {}
    for col in columns:
        return_value[col] = df[col]

    return return_value


if __name__ == "__main__":
    read()
