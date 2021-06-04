#!/usr/bin/env python3

import sys
from datetime import datetime
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


def mean(df: pd.DataFrame, title_count: int, bbg: Optional[str]) -> float:
    if bbg:
        df = df[df["bbg"].str.startswith(bbg)]

    return len(df) / title_count


def main():
    title_count = 0
    with open("stats/title_count.csv", "r") as f:
        title_count = int(f.read())

    # GND-Stammdaten (ID (gnd_id), Erfassungsdatum (ser) und URL (uri))
    gnd_data = pd.read_csv("data/gnd.csv", low_memory=False)

    gnd_data["created_at"] = pd.to_datetime(
        gnd_data["ser"].str[-8:], format="%d-%m-%y", errors="coerce"
    )

    # Verknüpfungen von DNB-Titeldaten aus den Feldern `0XXX $9`.
    title_links = pd.read_csv(
        "data/0XXX_9.csv", low_memory=False, names=["idn", "gnd_id", "name"]
    )

    df = pd.merge(title_links, gnd_data[["gnd_id", "bbg"]], on="gnd_id", how="left")
    df = df[pd.notna(df.bbg) & df["bbg"].str.startswith("T")]

    # Anzahl der Verknüpfungen von DNB-Titeln und GND-Entitäten.
    with open("stats/title_gnd_links.csv", "w") as f:
        f.write(str(len(df)))

    # Anzahl an verknüpften GND-Entitäten mit DNB-Titeln (unique).
    with open("stats/title_gnd_links_unique.csv", "w") as f:
        f.write(str(len(df["gnd_id"].unique())))

    # TOP-10 verknüpfte Entitäten
    gnd_top10 = top10(df, None)
    gnd_top10[:10].to_csv("stats/title_gnd_top10.csv")

    for bbg in ["Tb", "Tf", "Tg", "Tp", "Ts", "Tu"]:
        Tx_top10 = top10(df, bbg)
        Tx_top10[:10].to_csv(f"stats/title_gnd_top10_{bbg}.csv")

    # Durchschnittliche Anzahl an Verknüpfungen pro DNB-Titel
    with open("stats/title_gnd_mean.csv", "w") as f:
        f.write(str(mean(df, title_count, None)))

    for bbg in ["Tb", "Tf", "Tg", "Tp", "Ts", "Tu"]:
        Tx_mean = mean(df, title_count, bbg)

        with open(f"stats/title_gnd_mean_{bbg}.csv", "w") as f:
            f.write(str(Tx_mean))

    # TOP-10 verknüpfte Entitäten (2021)
    gnd_2021 = gnd_data[
        (gnd_data["created_at"] >= "2021-01-01")
        & (gnd_data["created_at"] <= "2021-12-31")
    ]

    df_2021 = df[df["gnd_id"].isin(gnd_2021["gnd_id"])]

    gnd_top10 = top10(df_2021, None)
    gnd_top10[:10].to_csv("stats/title_gnd_newcomer_top10.csv")

    for bbg in ["Tb", "Tf", "Tg", "Tp", "Ts", "Tu"]:
        Tx_top10 = top10(df_2021, bbg)
        Tx_top10[:10].to_csv(f"stats/title_gnd_newcomer_top10_{bbg}.csv")

    # Maschinell verknüpft
    df = pd.read_csv(
        "data/044H_9.csv", low_memory=False, names=["idn", "gnd_id", "name"]
    )
    with open("stats/title_gnd_links_auto.csv", "w") as f:
        f.write(str(len(df)))

    # Aus Fremddaten
    df = pd.read_csv(
        "data/044K_9.csv", low_memory=False, names=["idn", "gnd_id", "name"]
    )
    with open("stats/title_gnd_links_ext.csv", "w") as f:
        f.write(str(len(df)))


if __name__ == "__main__":
    main()
