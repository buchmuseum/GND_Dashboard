#!/usr/bin/env python3

import sys
from typing import Optional

import pandas as pd


def main():
    df_022R = pd.read_csv("data/user/022R.csv", low_memory=False)
    df_028R = pd.read_csv("data/user/028R.csv", low_memory=False)
    df_029R = pd.read_csv("data/user/029R.csv", low_memory=False)
    df_030R = pd.read_csv("data/user/030R.csv", low_memory=False)
    df_041R = pd.read_csv("data/user/041R.csv", low_memory=False)
    df_065R = pd.read_csv("data/user/065R.csv", low_memory=False)

    df_0XXR = pd.concat([df_022R, df_028R, df_029R, df_030R, df_041R, df_065R])

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

    # for bbg in ["Tb", "Tf", "Tg", "Tp", "Ts", "Tu"]:
    #     Tx_top10 = top10(df, bbg)
    #     Tx_top10[:10].to_csv(f"stats/title_gnd_top10_{bbg}.csv")

    # AUSWERTUNG GND-SYSTEMATIK
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
