interval = [134564, 585159]

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0

def meetCriteria(n):
    str_n = str(n)

    adj_cond = False
    isMonotonic = True
    adj_groups = {} # Not elegant but okay
    for c, c_n in zip(str_n, str_n[1:]):
        # Check if sequence is monotonic
        if sign(int(c_n) - int(c)) == -1:
            isMonotonic = False
            break

        if c == c_n:
            if c not in adj_groups.keys():
                adj_groups[c] = 1
            adj_groups[c] += 1
            adj_cond = True

    groupWithOnlyTwo = False
    for v in adj_groups.values():
        if v == 2:
            groupWithOnlyTwo = True
            break

    if adj_cond and isMonotonic and groupWithOnlyTwo:
        return True
    else:
        return False
 
#print(meetCriteria(123666))
count = 0
for n in range(interval[0], interval[1]):
    if meetCriteria(n):
        count += 1

print(count)
