import numpy as np
import math

with open("input.txt", "r") as f:
    lines = f.readlines()
    field = [l.strip('\n') for l in lines]

print('\n'.join(field))

#field = [".#..#",
#         ".....",
#        "#####",
#        "....#",
#        "...##"]

count_f = np.zeros((len(field), len(field[0])))
width = count_f.shape[1]
height = count_f.shape[0]
# Find all asteroids
asteroids_pos = []
for y, line in enumerate(field):
    for x, a in enumerate(line):
        if a == '#':
            asteroids_pos.append((x, y))

print(len(asteroids_pos))
best_asteroid = None
best_count = 0
for asteroid1 in asteroids_pos:
    seen_angles = []
    for asteroid2 in asteroids_pos:
        if asteroid1 == asteroid2:
            continue

        x = asteroid2[0] - asteroid1[0]
        y = asteroid2[1] - asteroid1[1]
        angle = math.atan2(y, x)

        if angle not in seen_angles:
            seen_angles.append(angle)
            count_f[asteroid1[1], asteroid1[0]] += 1

    if count_f[asteroid1[1], asteroid1[0]] > best_count:
        best_count = count_f[asteroid1[1], asteroid1[0]]
        best_asteroid = asteroid1

print(best_count, best_asteroid)
print(count_f)
