with open("input.txt", "r") as f:
    data = [int(v) for v in f.readline().strip('\n')]

width = 25
height = 6

col = 0
layer = []
img = []
print(len(data))
curr_h = 0
curr_layer = 0
l_with_fewest_zero = None
fewest_zero = float('inf')
for i, j in zip(range(0, len(data), width), range(width, len(data)+1, width)):
    layer.append(data[i:j])
    
    curr_h += 1
    if curr_h == height:
        img.append(layer)

        z_count = 0
        for y in range(len(layer)):
            for x in range(len(layer[0])):
                if layer[y][x] == 0:
                    z_count += 1

        if z_count < fewest_zero:
            l_with_fewest_zero = curr_layer
            fewest_zero = z_count

        layer = []
        curr_h = 0
        curr_layer += 1


print("Number of layers:", len(img))
print("Height:", len(img[0]))
print("Width:", len(img[0][0]))
print(f"Layer with fewest zeros is {l_with_fewest_zero} with {fewest_zero} zeros.")

# Find number of 1s and 2s
one_count = 0
two_count = 0
for y in range(len(img[l_with_fewest_zero])):
    for x in range(len(img[l_with_fewest_zero][0])):
        if img[l_with_fewest_zero][y][x] == 1:
            one_count += 1
        elif img[l_with_fewest_zero][y][x] == 2:
            two_count += 1

print(f"Answer: {one_count * two_count}.")
