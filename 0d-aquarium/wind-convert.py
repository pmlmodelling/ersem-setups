import numpy as np
import pandas as pd
import os


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
meteo_file = os.path.join(parent_dir,
                          "L4",
                          "L4_meteo_2002-2020_1hours.dat")

names = ["Date", "Time", "wind_x",
         "wind_y", "pressure", "air temp",
         "dew temp", "cloudi cover"]

df = pd.read_csv(meteo_file,
                 delimiter="\s+| |  | ",
                 engine="python",
                 names=names)


df["wind"] = df.apply(
    lambda row: np.sqrt(float(row.wind_x)**2 + float(row.wind_y)**2),
    axis=1)

df[["Date", "Time", "wind"]].to_csv("wind.dat",
                                    sep=" ",
                                    header=False,
                                    index=False)
