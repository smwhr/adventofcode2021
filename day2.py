import pandas as pd

df = (pd
        .read_csv("data2.lst", header=None, delim_whitespace=True)
        .rename(columns = {0: "direction", 1: "norm"})
    )

z = (   df.query("direction == 'down'")['norm'].sum()
    -  df.query("direction == 'up'")['norm'].sum()
)

x = df.query("direction == 'forward'")['norm'].sum()

print(f"Part 1 : {x * z}")

df["aimvar"] = 0
df["aimvar"] = df["aimvar"].mask(df.direction == 'up', -df.norm)
df["aimvar"] = df["aimvar"].mask(df.direction == 'down', df.norm)
df["xvar"] = 0
df["xvar"] = df["xvar"].mask(df.direction == 'forward', df.norm)

df["aim"] = df["aimvar"].cumsum()
df["zvar"] = df["xvar"] * df["aim"]

x = df["xvar"].sum()
z = df["zvar"].sum()

print(f"Part 2 : {x * z}")
