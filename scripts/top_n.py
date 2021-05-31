#!/usr/bin/env python3

import sys

import pandas as pd


def main():
    df = pd.read_csv(
        sys.argv[1], low_memory=False, usecols=["idn", "gnd_id", "bbg", "name"]
    )
    df = df[pd.notna(df["bbg"])]

    n = int(sys.argv[2])

    if len(sys.argv) == 4:
        df = df[df["bbg"].str.startswith(sys.argv[3])]

    df["count"] = 1

    df_grouped = (
        df.groupby(by=["gnd_id", "name", "bbg"])
        .sum()
        .sort_values("count", ascending=False)
    )

    # df_grouped.to_csv(


if __name__ == "__main__":
    main()
