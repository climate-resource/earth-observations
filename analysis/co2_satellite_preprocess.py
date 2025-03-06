import os
import numpy as np
import pandas as pd

from netCDF4 import Dataset


# extract all file names from downloaded folder
all_files=os.listdir("../datasets/downloads/30e7ca145a49496e137a0ce5b6c1295")

# initialize result dictionary
df_dict={}
file0=Dataset(f"../datasets/downloads/30e7ca145a49496e137a0ce5b6c1295/{all_files[0]}")
for key in file0.variables:
    if len(file0.variables[key][:].shape) < 2:
        df_dict[key]=[]
        df_dict["day"]=[]
        df_dict["month"]=[]
        df_dict["year"]=[]

# populate result dictionary
for i,file in enumerate(all_files):
    if i==1:
        continue
    day=[file.split("-")[0][-2:]]
    month=[file.split("-")[0][4:6]]
    year=[file.split("-")[0][:4]]

    # Open a .nc file ("file_name")
    file = Dataset(f"../datasets/downloads/30e7ca145a49496e137a0ce5b6c1295/{file}")
    for j,key in enumerate(file.variables):

        dat = file.variables[key][:].data
        if len(file.variables[key][:].shape) < 2:
            df_dict[key].append(dat)
    df_dict["day"].append(day*len(dat))
    df_dict["month"].append(month*len(dat))
    df_dict["year"].append(year*len(dat))

# ensure correct data format
for key in df_dict:
    df_dict[key]=np.concatenate(df_dict[key])

# create pandas dataframe
df = pd.DataFrame(df_dict)
df[["day","month","year"]]=df[["day","month","year"]].apply(pd.to_numeric)

# save as csv
df.to_csv("../datasets/preprocessed_data/monthly_co2_airs_nlis.csv")
