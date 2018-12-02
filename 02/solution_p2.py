import sys
lines = list(sys.stdin)
found = False
for test1 in lines:
    for test2 in lines:
        if test1 == test2:
            continue
        wrong = None
        many_wrong = False
        assert len(test1) == len(test2)
        for i, letter in enumerate(test1):
            if test2[i] != letter:
                if wrong is not None:
                    many_wrong = True
                wrong = i
        if not many_wrong:
            found = True
            break
    if found:
        break
print(test1[:wrong] + test1[wrong + 1:])
