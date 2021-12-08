import pandas as pd

f = open("data8.lst")

lines = [l.strip("\n") for l in f.readlines()]

df = pd.DataFrame(columns=list("ABCD"))

def append_dict(df, values):
    return df.append(dict(zip(list("ABCD"),values)), ignore_index=True)

for l in lines:
    left, right = l.split("|")
    right_values = right.strip().split(" ") 
    df = append_dict(df, right_values)


def len_to_digit(n):
    if n == 2:
        return "1"
    if n == 4:
        return "4"
    if n == 3:
        return "7"
    if n == 7:
        return "8"
    return pd.NA

#    aaaa
#   b    c
#   b    c
#    dddd 
#   e    f
#   e    f
#    gggg 

X_TO_D = {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg"
    }
D_TO_X = {v: k for k, v in X_TO_D.items()}

def len_to_correct(n):
    if n == 2:
        return "cf" #"1"
    if n == 4:
        return "bcdf" #"4"
    if n == 3:
        return "acf" #"7"
    if n == 7:
        return "abcdefg" #"8"
    return None


df2 = df.applymap(lambda x : len_to_digit(len(x)) )

total_of_1478 = df2.agg("count").sum()
print(f"1: {total_of_1478}")

def infer(data_left):
    # first pass : infer obvious
    mapping = {l : set(list("abcdefg")) for l in list("abcdefg")}

    for x in data_left:
        correct = len_to_correct(len(x))
        if correct is not None:
            # x = "ab"
            # correct = "cf"
            for l in mapping:
                [mapping[l].discard(n) for n in list("abcdegf") 
                        if (l in list(x) and n not in list(correct))
                        or (l not in list(x) and n in list(correct))
                ]
    
    

    def _test(possible_mapping):
        for x in data_left:
            decoded = decode(x, possible_mapping)
            if decoded not in X_TO_D.values():
                return False
        return True

    def _traverse(inputs, collected_mapping):
        if(len(inputs) == 0):
            return collected_mapping if len(collected_mapping) == 7 and _test(collected_mapping) else None
        
        current_letter = inputs[0]
        possible_letters = [x for x in mapping[current_letter] if x not in collected_mapping.values()]
        if len(possible_letters) == 0:
            return None

        for x in possible_letters:
            possible_mapping = _traverse(inputs[1:], {**collected_mapping, **{current_letter:x}})
            if possible_mapping is not None and len(possible_mapping) == 7:
                return possible_mapping
        return collected_mapping

    unique_mapping = _traverse(list("abcdefg"), {})
    return unique_mapping

def decode_unsorted(x, mapping):
    return "".join([mapping[i] for i in list(x)])

def decode(x, mapping):
    return "".join(sorted([mapping[i] for i in list(x)]))

def lst_to_int(lst):
    return int("".join([str(c) for c in lst]))

def unit():
    # test = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    # test = "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe"
    test = "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc"
    left, right = test.split("|")
    data_left   = left.strip().split(" ")
    data_right  = right.strip().split(" ")
    mapping = infer(data_left)

    # print([D_TO_X[d] for d in [decode(x, mapping) for x in data_left]])
    print(data_right)
    print([decode_unsorted(x, mapping) for x in data_right])
    print(lst_to_int([D_TO_X[d] for d in [decode(x, mapping) for x in data_right]]))

# unit()

# breakpoint()
somme = 0
for l in lines:
    left, right = l.split("|")
    data_left = left.strip().split(" ") 
    data_right = right.strip().split(" ") 
    mapping = infer(data_left + data_right)
    #print(mapping)
    n = lst_to_int([D_TO_X[d] for d in [decode(x, mapping) for x in data_right]])
    # print([decode(x, mapping) for x in data_right], ":", n)
    somme += n
print(somme)
