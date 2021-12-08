import pandas as pd
import numpy as np

f = open("data7.lst")

initial_numbers = np.asarray(f.readlines()[0].strip("\n").split(","), dtype=int)

df = pd.DataFrame({"position": initial_numbers})

n = None
f = np.Infinity

for i in range(0, df.max().position):
    #df["exp"] = abs(df["position"] - i)
    dst = abs(df["position"] - i)
    df["exp"] = (dst * (dst + 1))//2
    exp = df["exp"].sum()
    #print(f"exp is {exp} for pos {i}")
    if exp < f :
        n = i
        f = exp

print(n, f)

breakpoint()