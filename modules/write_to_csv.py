import pandas as pd


def write_data(file_path, key, value):
  df = pd.read_csv(file_path)

  results = pd.DataFrame([value], columns=key)

  df = pd.concat([df, results])
  df.to_csv(file_path, index=False)
  print("success writing to %s" % file_path)


if __name__ == "__main__":
  write_data()
