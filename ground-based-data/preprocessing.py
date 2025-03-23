import xarray as xr
from pathlib import PureWindowsPath
import itertools
import pandas as pd
import os

data_path = "../../../.esgpull/data/input4MIPs"

def prep_data(sub_set=False, filter_year=2002):
    for era, gas, id, cmip_version, version in itertools.product(
            ["CMIP6Plus", "CMIP7"], ["ch4", "co2"],
            ["000101-202212", "000101-099912", "100001-174912", "175001-202212"],
            ["0-3-0", "1-0-0", "0-4-0"],
            ["v20240806", "v20250228", "v20241205"]
    ):
        freq = "mon"
        p = f"/{era}/CMIP/CR/CR-CMIP-{cmip_version}/atmos/{freq}/{gas}/gm/{version}/{gas}_input4MIPs_GHGConcentrations_CMIP_CR-CMIP-{cmip_version}_gm_{id}.nc"

        try:
            xr.open_dataset(data_path + p)
        except:
            continue
        else:
            d = xr.open_dataset(PureWindowsPath(data_path + p))
            try:
                pd.DatetimeIndex(d.time)
            except:
                df = pd.DataFrame(
                dict(
                    year=[d.time.values[i].year for i in range(len(d.time))],
                    month=[d.time.values[i].month for i in range(len(d.time))],
                    day=[d.time.values[i].day for i in range(len(d.time))],
                    )
                )
            else:
                dat = pd.DatetimeIndex(d.time)
                df = pd.DataFrame(
                    dict(
                        year=dat.year.values,
                        month=dat.month.values,
                        day= dat.day.values
                    )
                )

            if gas == "ch4":
                df["values"] = d.ch4.values
            elif gas == "co2":
                df["values"] = d.co2.values
            else:
                raise ValueError("Unknown gas type")
            df["version"]=version+"-"+cmip_version
            df["gas"]=gas
            df["freq"]=freq
            df["era"]=era
            if len(df) > 0:
                df.to_csv("ground-based-data/datasets/" + gas + "_" + era + "_" + freq + "_" + id + "_" + version + ".csv")

            if sub_set:
                df_filter = df[df["year"] > filter_year]
                if len(df_filter) > 0:
                   # print(list(df_filter.columns.drop(["day", "values"]).values))
                    df_prep = df_filter.groupby(list(df_filter.columns.drop(["day", "values"]).values)).agg({"values": "mean"}).reset_index()
                    df_prep["year_month"] = df_prep["year"].values.astype(str) + "-" + df_prep["month"].values.astype(str)
                    #df_prep.drop(["year", "month"])
                    df_prep.to_csv("ground-based-data/datasets/prep_" + gas + "_" + era + "_" + freq + "_" + id + "_" + version + ".csv")

prep_data(sub_set=True, filter_year=2002)


def joined_data(gas):
    counter = 0
    for file in os.listdir("ground-based-data/datasets"):
        if file.startswith(f"prep_{gas}"):
            df = pd.read_csv(f"ground-based-data/datasets/{file}").drop("Unnamed: 0", axis=1)
            if counter == 0:
                df1 = df
            else:
                df1 = df1.merge(df, how="outer")
            counter += 1
    df1.to_csv(f"ground-based-data/datasets/agg_{gas}_2003-present.csv")

joined_data("ch4")
joined_data("co2")