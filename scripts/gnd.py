#!/usr/bin/env python3

import sys

import pandas as pd


def main():
    df = pd.read_csv(sys.argv[1], low_memory=False, names=["id", "count"])
    names = pd.read_csv(
        "data/gnd_systematik_names.csv", low_memory=False, names=["id", "name"]
    )

    result = pd.merge(df, names, on="id", how="left")
    result.to_csv("stats/gnd_classification_all.csv", index=False)

    result = result[["id", "name", "count"]][:10]
    result.to_csv("stats/gnd_classification_top10.csv", index=False)


if __name__ == "__main__":
    main()
