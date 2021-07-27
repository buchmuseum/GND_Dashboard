#!/usr/bin/env python3

import sys
from typing import Optional

import pandas as pd


def main():
    gnd_data = pd.read_csv("data/user/gnd.csv", low_memory=False)

    df_0XXR = pd.read_csv(
        "data/user/0XXR.csv", names=["idn", "gnd_id", "name", "code"], low_memory=False
    )

    df_0XXR = pd.merge(df_0XXR, gnd_data[["gnd_id", "bbg"]], on="gnd_id", how="left")

    # AUSWERTUNG RELATIONS-CODES

    df_codes = (
        df_0XXR[["idn", "code"]]
        .groupby(by="code")
        .count()
        .sort_values("idn", ascending=False)
    )
    df_codes = df_codes.rename(columns={"idn": "count"})
    df_codes.to_csv("stats/gnd_codes_all.csv")
    df_codes[:10].to_csv("stats/gnd_codes_top10.csv")

    # AUSWERTUNG GND-SYSTEMATIK
    df = pd.read_csv(
        "stats/gnd_systematik.csv", low_memory=False, names=["id", "count"]
    )
    names = pd.read_csv(
        "data/gnd_systematik_names.csv", low_memory=False, names=["id", "name"]
    )

    result = pd.merge(df, names, on="id", how="left")
    result.to_csv("stats/gnd_classification_all.csv", index=False)

    result = result[["id", "name", "count"]][:10]
    result.to_csv("stats/gnd_classification_top10.csv", index=False)

    # AUSWERTUNG GND-SYSTEMATIK (nur Ts*)
    df = pd.read_csv(
        "stats/gnd_systematik_Ts.csv", low_memory=False, names=["id", "count"]
    )

    result = pd.merge(df, names, on="id", how="left")
    result.to_csv("stats/gnd_classification_Ts_all.csv", index=False)


if __name__ == "__main__":
    main()
