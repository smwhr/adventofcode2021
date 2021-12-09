import pandas as pd
import numpy as np

f = open("data9.lst")

lines = [l.strip() for l in f.readlines()]

HEIGHT = len(lines)
WIDTH  = len(lines[0])

NEIGH_COLS = {"tm": "Int64", "l": "Int64", "r": "Int64", "bm": "Int64"}
DIRECT_NEIGH = ["tm","l","r","bm"]

LEFT_COLS = ["l"] #["tl", "l", "bl"]
RIGHT_COLS = ["r"] #["tr", "r", "br"]
TOP_COLS = ["tm"] #["tl", "tm", "tr"]
BOT_COLS = ["bm"] #["bl", "bm", "br"]

values = np.asarray(list("".join(lines)), dtype=int)
df = pd.DataFrame({'h':  values}).reset_index().rename({'index':'i'}, axis = 'columns')

#df["tl"] = df["h"].shift(WIDTH+1)
df["tm"] = df["h"].shift(WIDTH)
#df["tr"] = df["h"].shift(WIDTH-1)

df["l"] = df["h"].shift(1)
df["r"] = df["h"].shift(-1)

#df["bl"] = df["h"].shift(-WIDTH+1)
df["bm"] = df["h"].shift(-WIDTH)
#df["br"] = df["h"].shift(-WIDTH-1)

df = df.astype(dtype=NEIGH_COLS)


df[TOP_COLS] = df[["i"] + TOP_COLS].mask(lambda df: df["i"] // WIDTH == 0, pd.NA)[TOP_COLS]
df[BOT_COLS] = df[["i"] + BOT_COLS].mask(lambda df: df["i"] // WIDTH == HEIGHT, pd.NA)[BOT_COLS]

df[LEFT_COLS] = df[["i"] + LEFT_COLS].mask(lambda df: df["i"] % WIDTH == 0, pd.NA)[LEFT_COLS]
df[RIGHT_COLS] = df[["i"] + RIGHT_COLS].mask(lambda df: df["i"] % WIDTH == WIDTH-1, pd.NA)[RIGHT_COLS]



df["min_neigh"] = df[DIRECT_NEIGH].min(axis=1)
df["is_min"] = df["h"] < df["min_neigh"]
df["risk"] = df["h"] + 1

df = df.astype(dtype={
        "min_neigh": "Int64",
        "is_min": bool,
        "risk": "Int64",
    })

print(df[df["is_min"]]["risk"].sum())

df["basin"] = df["i"]
df = df.astype(dtype={"basin": "Int64"})
df["basin"] = df[["i", "is_min", "basin"]].mask(lambda df: df["is_min"] == False, pd.NA)["basin"]

filled = df["basin"].count()

def neighs(i):
    return [j for j in [
        None if (i) // WIDTH == 0 else i - WIDTH,
        None if (i) // WIDTH == HEIGHT else i + WIDTH,
        None if i  % WIDTH  == 0 else i -1,
        None if i  % WIDTH  == WIDTH -1 else i + 1,
    ] if j is not None]


while True:
    basined = df[["i", "basin"]].dropna()
    for i in list(basined["i"]):
        ns = neighs(i)
        for n in ns:
            if df.loc[df["i"] == n]["h"].max() == 9:
                continue
            if df.loc[df["i"] == n]["basin"].any():
                continue
            df.loc[df["i"] == n,"basin"] = basined.loc[i]["basin"]
    
    newfilled = df["basin"].count()
    print(newfilled - filled)

    if  newfilled == filled:
        break
    filled = newfilled

res = df.groupby("basin").agg({"i":"count"}).sort_values("i", ascending=False)[:3].prod()
print(res.i)