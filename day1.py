import pandas as pd

df = pd.read_csv("data1.lst", header=None, delim_whitespace=True)
df["ori"] = df[0]
df["shi"] = df["ori"].shift(1)
df = df.assign(inc=lambda df: df["ori"] > df["shi"])

print(df["inc"].sum())

df["shi2"] = df["ori"].shift(2)
df = df.assign(su3 = lambda df: df["ori"] + df["shi"] + df["shi2"])
df["su3shi"] = df["su3"].shift(1)
df = df.assign(incsu3=lambda df: df["su3"] > df["su3shi"])

print(df["incsu3"].sum())