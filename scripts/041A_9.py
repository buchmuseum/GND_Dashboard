#!/usr/bin/env python3

import sys

import pandas as pd


def main():
    df = pd.read_csv(sys.argv[1], low_memory=False)

    with open("stats/link_count.csv", "w") as f:
        f.write(str(len(df)))

    with open("stats/link_count_unique.csv", "w") as f:
        f.write(str(len(df["gnd_id"].unique())))


if __name__ == "__main__":
    main()
