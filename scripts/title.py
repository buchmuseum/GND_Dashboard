#!/usr/bin/env python3

import sys
from typing import Optional

import pandas as pd


def top10(df: pd.DataFrame, bbg: Optional[str]) -> pd.DataFrame:
    df_top10 = df[["gnd_id", "bbg", "name"]]

    if bbg:
        df_top10 = df_top10[df_top10["bbg"].str.startswith(bbg)]

    df_top10["count"] = 1
    df_top10 = (
        df_top10.groupby(by=["gnd_id", "bbg", "name"])
        .sum()
        .sort_values("count", ascending=False)
    )

    return df_top10


def mean(df: pd.DataFrame, bbg: Optional[str]) -> float:
    if bbg:
        df = df[df["bbg"].str.startswith(bbg)]

    df_mean = df[["idn", "gnd_id"]].groupby(by="idn").count()

    return df_mean["gnd_id"].mean()


def main():
    df = pd.read_csv(sys.argv[1], low_memory=False)
    df = df[pd.notna(df["bbg"])]

    # Anzahl der Verknüpfungen von DNB-Titeln und GND-Entitäten.
    with open("stats/title_gnd_links.csv", "w") as f:
        f.write(str(len(df)))

    # Anzahl an verknüpften GND-Entitäten mit DNB-Titeln (unique).
    with open("stats/title_gnd_links_unique.csv", "w") as f:
        f.write(str(len(df["gnd_id"].unique())))

    # TOP-10 verknüpfte Entitäten
    gnd_top10 = top10(df, None)
    gnd_top10[:10].to_csv("stats/gnd_top10.csv")

    for bbg in ["Tb", "Tf", "Tg", "Tp", "Ts", "Tu"]:
        Tx_top10 = top10(df, bbg)
        Tx_top10[:10].to_csv(f"stats/{bbg}_top10.csv")

    # Durchschnittliche Anzahl an Verknüpfungen pro DNB-Titel
    with open("stats/gnd_mean.csv", "w") as f:
        f.write(str(mean(df, None)))

    for bbg in ["Tb", "Tf", "Tg", "Tp", "Ts", "Tu"]:
        Tx_mean = mean(df, bbg)

        with open(f"stats/{bbg}_mean.csv", "w") as f:
            f.write(str(Tx_mean))


if __name__ == "__main__":
    main()
