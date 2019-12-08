import numpy as np 

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
for i, j in zip(range(0, len(data), width), range(width, len(data)+1, width)):
    layer.append(data[i:j])
    
    curr_h += 1
    if curr_h == height:
        img.append(layer)


        layer = []
        curr_h = 0
        curr_layer += 1

print("Number of layers:", len(img))
print("Height:", len(img[0]))
print("Width:", len(img[0][0]))

decoded_img = np.ones((len(img[0]), len(img[0][0]))) * 2
print(decoded_img[:5, :5])
print(decoded_img.shape)
for layer in range(len(img)):
    for y in range(len(img[0])):
        for x in range(len(img[0][0])):
            p = img[layer][y][x]

            # If transparent, overwrite
            if decoded_img[y, x] == 2:
                decoded_img[y, x] = p

print(decoded_img.astype("int"))
