import pandas as pd


df = pd.read_csv("data3.lst", 
                header=None, delim_whitespace=True, 
                dtype='string')

bitlen = len(df[0].iloc[0])
gamma   = ""
epsilon = ""

for i in range(0,bitlen):
    df[i+1] = df[0].str[i]
    gamma += df[i+1].value_counts().idxmax()
    epsilon += df[i+1].value_counts().idxmin()

breakpoint()


print(f"gamma : {int(gamma, 2)}")
print(f"epsilon : {int(epsilon, 2)}")
print("======")
print(f"multiply : {int(gamma, 2) * int(epsilon, 2)}")



oxyframe = df
for i in range(0,bitlen):
    freqs = oxyframe[i+1].value_counts()
    bitcrit = '1' if freqs[0] == freqs[1] and freqs[1] > 0 else freqs.idxmax()
    oxyframe = oxyframe[oxyframe[i+1] == bitcrit]

coframe = df
for i in range(0,bitlen):
    freqs = coframe[i+1].value_counts()
    bitcrit = '0' if len(freqs) > 1 and freqs[0] == freqs[1] else freqs.idxmin()
    coframe = coframe[coframe[i+1] == bitcrit]

oxy = int(oxyframe[0].iloc[0], 2)
co2 = int(coframe[0].iloc[0], 2)

print(oxy * co2)

breakpoint()