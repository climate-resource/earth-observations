# imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# select satellite
select_satellite = "emma"  # either "scimanchy" or "airs" or "emma"
# load dataset
if select_satellite == "scimanchy":
    measure="XCO"
    df = pd.read_csv("../data/scimanchy_besd_df.csv")
elif select_satellite == "airs":
    measure="CO"
    df = pd.read_csv("../data/airs_nils_df.csv")
elif select_satellite == "emma":
    measure="XCO"
    df = pd.read_csv("../data/merged_emma_df.csv")
else:
    raise ValueError("Select satellite")

# select data of northern hemisphere
df_north = df[df["lat"]>0]
# average CO2 measures across days for each month
df_north_agg = df_north.groupby(["year", "month"]).agg({"co2": "mean"}).reset_index()
# composite column of year-month
df_north_agg["month-year"] = [df_north_agg.month.astype(str)[i]+"/"+df_north_agg.year.astype(str)[i][-2:] for i in range(len(df_north_agg.month))]

# plot and save data
fig, axs = plt.subplots(1,1, figsize=(7,3))
axs.plot(df_north_agg["month-year"], df_north_agg["co2"])
axs.tick_params("x", labelsize=7, rotation=90)
axs.set_ylabel(fr"${measure}_2$ in ppm")
axs.set_title(select_satellite+"; monthly avg. CO2 values; northern hemisphere")
fig.savefig(f"{select_satellite}_trend_{measure}2.png")


# %% Plot seasonal cycle of CO2
df2 = df
df2["hemisphere"] = np.where(df2["lat"]<0, "south", "north")

g = sns.relplot(x="month", y="co2", hue="year", col="hemisphere", data=df2,
                kind="line")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle(rf"{select_satellite}; Seasonal cycle of ${measure}_2$")
g.fig.savefig(f"{select_satellite}_seasonalcycle_{measure}2.png")
