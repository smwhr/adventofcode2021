import pandas as pd
import numpy as np
import functools

f = open("data6.lst")

initial_numbers = np.asarray(f.readlines()[0].strip("\n").split(","), dtype=int)

initial = pd.DataFrame({"age": initial_numbers})

df = initial.groupby("age").agg({"age": "count"}).rename(columns={"age": "num"}).astype({"num": "Int64"})


for i in range(0, 9):
    if i not in df.index:
        df.loc[i] = 0
        
df = df.sort_index(ascending=False)


def inc(df):
    newdf = df.copy()
    mothering = newdf.loc[0]
    newdf["num"] = newdf["num"].shift(1)
    newdf.loc[8] = mothering
    newdf.loc[6] += mothering

    return newdf

for i in range(0,256):
    df = inc(df)

print(df["num"].sum())

breakpoint()