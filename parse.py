import pandas as pd


def read_data(filename: str) -> pd.DataFrame:
    def parse(line):
        date, *variables = line.split(",")
        variables = map(
            lambda text: float("".join(filter(str.isdigit, text))) / 1000,
            variables[1::2],
        )
        return [date] + list(variables)

    with open(filename, encoding="utf-8") as data:
        header, *lines = data.readlines()
        columns = header.split(",")[:-1]
        rows = list(map(parse, lines))
        return pd.DataFrame(rows, columns=columns)


def add_lags(data: pd.DataFrame, max_lag: int) -> pd.DataFrame:
    data = data.drop(columns="Date", errors="ignore")
    dataframes = []
    for i in range(max_lag + 1):
        shifted = data.shift(-i)[: len(data) - max_lag]
        shifted.columns = pd.Index(
            [f"{name.replace(' ', '_')}-{i}" for name in shifted.columns]
        )
        dataframes.append(shifted)
    return pd.concat(dataframes, axis=1)


data = read_data("raw_data.csv")[:-37]  # to remove missing Stoicism values
print(data.describe())
print(data.shape)
data = add_lags(data, 2)
print(data.shape)
print(data.describe())
data.to_csv("dataset.csv")
