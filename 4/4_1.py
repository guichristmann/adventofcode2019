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
    for c, c_n in zip(str_n, str_n[1:]):
        # Check if sequence is monotonic
        if sign(int(c_n) - int(c)) == -1:
            isMonotonic = False
            break

        # Checking if two adjacent digits are the same
        if c == c_n:
            adj_cond = True

    if adj_cond and isMonotonic:
        return True
    else:
        return False
 
count = 0
for n in range(interval[0], interval[1]):
    if meetCriteria(n):
        count += 1

print(count)
