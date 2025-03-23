# imports
import numpy as np
import pandas as pd
import geopandas as gpd
import geodatasets as gd
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
    df_raw = pd.read_csv("../data/merged_emma_df.csv")

    df_raw["long_new"] = df_raw["long"].round()
    df_raw["lat_new"] = df_raw["lat"].round()
    df_raw["month"] = pd.Series(np.where(df_raw["month"] <= 6., "Jan-Jun", "Jul-Dec"))
    # grid observations
    df = df_raw.groupby(["long_new", "lat_new", "year", "month"]).agg({"co2": "mean"}).reset_index()
    df.rename(columns={"long_new": "long", "lat_new": "lat"}, inplace=True)

else:
    raise ValueError("Select satellite")

# load the low resolution world map
world = gpd.read_file(gd.get_path("naturalearth.land"))

# instantiate figure
fig = plt.figure(figsize=(7, 4))

for y in np.arange(2003, 2022, 1):
    for k in ["Jan-Jun", "Jul-Dec"]:# range(1, 13):
        # select data
        df2 = df[(df.year == y) & (df.month == k)]
        if len(df2) == 0:
            continue
        gdf = gpd.GeoDataFrame(
            df2,
            geometry=gpd.points_from_xy(df2.long, df2.lat),
            crs="EPSG:4326",
        )
        # add axes to figure
        ax = fig.add_subplot()
        # plot a basic map of the world
        world.plot(ax=ax, color="lightgray", edgecolor="black", alpha=0.5)
        # add satellite observations
        gdf.plot(
            column="co2",
            ax=ax,
            legend=True,
            cmap="cool",
            markersize=2,
            alpha=0.1,
            legend_kwds={
                "label": rf"${measure}_2$ in ppm",
                "orientation": "vertical",
                "shrink": 0.65,
            },
            vmax=np.max(df["co2"]),
            vmin=np.min(df["co2"]),
        )
        # add horizontal line for equator
        ax.axhline(0, color="red", linewidth=1)
        # add grid with 15 degrees for longitudes and latitudes
        [ax.axhline(y=i, color="grey", alpha=0.3) for i in np.arange(-90, 90, 15)]
        [ax.axvline(x=i, color="grey", alpha=0.3) for i in np.arange(-210, 210, 15)]
        # set labels for x,y axis
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        # reduce tick size for plot and colorbar
        ax.tick_params(labelsize=7)
        cb_ax = fig.axes[1]
        cb_ax.tick_params(labelsize=7)
        # add title with information about year/month
        ax.set_title(
            rf"{select_satellite}; ${measure}_2$ in ppm for {np.unique(df2['year'])[0]}/{np.unique(df2['month'])[0]}"
        )
        ax.set_aspect(1)
        # show figure
        fig.show()
        fig.clear()
