# imports
import numpy as np
import pandas as pd
import geopandas as gpd
import geodatasets as gd
import matplotlib.pyplot as plt

# select satellite
select_satellite = "scimanchy"  # either "scimanchy" or "airs"

# load dataset
if select_satellite == "scimanchy":
    measure="XCO"
    df = pd.read_csv("../data/scimanchy_besd_df.csv")
    idx_time = (11, 13)
elif select_satellite == "airs":
    measure="CO"
    df = pd.read_csv("../data/airs_nils_df.csv")
    idx_time = (-8, -6)

# select one day/month/year
reduced_df = df[(df.day == 12) & (df.month==1) & (df.year == 2004)] #(df.month == 1) &
# extract hours of selected day and create new column in dataframe
hrs = [list(reduced_df["time"])[i][idx_time[0]:idx_time[1]] for i in range(len(reduced_df))]
reduced_df["hrs"] = hrs

# load the low resolution world map
world = gpd.read_file(gd.get_path("naturalearth.land"))

# instantiate figure
fig = plt.figure(figsize=(7, 4))

# plot data for each hour
for hr in np.unique(hrs):
    # select observations for target hour
    df2 = reduced_df[reduced_df["hrs"]==str(hr)]
    # create geopandas data frame
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
        markersize=14,
        alpha=0.9,
        legend_kwds={
            "label": rf"${measure}_2$ in ppm",
            "orientation": "vertical",
            "shrink": 0.65,
        },
        vmax=390,
        vmin=370,
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
    ax.set_xticks(np.arange(-210, 210, 15))
    ax.set_yticks(np.arange(-90, 90, 30))
    ax.set_ylim(-90, 90)
    ax.set_xlim(-210, 210)
    # add title with information about year/month/day + hour
    ax.set_title(
        rf"{select_satellite}; ${measure}_2$ in ppm for {np.unique(df2['year'])[0]}/{np.unique(df2['month'])[0]}/{np.unique(df2['day'])[0]}; {np.unique(df2['hrs'])[0]} hr"
    )
    ax.set_aspect(1)
    # show figure
    fig.show()
    fig.clear()
