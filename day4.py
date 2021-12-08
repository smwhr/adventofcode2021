from pandas.core.arrays.sparse import dtype
import numpy as np
import pandas as pd


f = open("data4.lst")

lines = [l.strip("\n") for l in f.readlines()]

draws = np.asarray(lines[0].split(","), dtype=int)

boards = [lines[i:i+5] for i in range(1, len(lines))[1::6]]

num_boards = len(boards)

board_points = np.concatenate([p for board in boards for p in [" ".join(board).split()] ]).astype(int)

df = (pd.DataFrame({"p":board_points})
        .reset_index().rename({'index':'i'}, axis = 'columns')
    )
df["b"] = df["i"] // 25                 #board number
df["c"] = df["i"] % 5                   #col number (in board)
df["r"] = df["i"] // 5                  #row number (global)
df["t"] = False

board_set = set(range(0,len(boards)))
lose_board = None

for draw in draws:
    df["t"] = df["t"].mask(df["p"] == draw, True)
    # fucking illisible a posteriori
    win_by_c = df.groupby(['b', 'c'], as_index=False)["t"].all().groupby(['b'], as_index=False)["t"].any().query("t == True")
    win_by_r = df.groupby(['b', 'r'], as_index=False)["t"].all().groupby(['b'], as_index=False)["t"].any().query("t == True")
    if len(win_by_c) > 0:
        [board_set.discard(i) for i in win_by_c["b"].index]
    if len(win_by_r) > 0:
        [board_set.discard(i) for i in win_by_r["b"].index]
    if(len(board_set) == 1):
        lose_board = list(board_set)[0]
    if(len(board_set) == 0):
        break

breakpoint()
unmarked_in_b = df[df["b"] == lose_board].query("t == False")["p"].sum()

print(draw * unmarked_in_b)
breakpoint()