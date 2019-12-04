with open("input.txt", "r") as f:
    lines = f.readlines()
    wire1 = lines[0].strip('\n').split(',')
    wire2 = lines[1].strip('\n').split(',')

#wire1 = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
#wire2 = ["U62","R66","U55","R34","D71","R55","D58","R83"]

#wire1 = ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
#wire2 = ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]

#wire1 = ["R8","U5","L5","D3"]
#wire2 = ["U7","R6","D4","L4"]

def get_coords(cmd_list):
    coords = [(0, 0)] 
    curr_pos = [0, 0]
    for cmd in cmd_list:
        direction = cmd[0]
        steps = int(cmd[1:])

        if direction == "U":
            curr_pos[1] += steps
        elif direction == "D":
            curr_pos[1] -= steps
        elif direction == "R":
            curr_pos[0] += steps
        elif direction == "L":
            curr_pos[0] -= steps

        coords.append(tuple(curr_pos))

    return coords

wire1_path = get_coords(wire1)
wire2_path = get_coords(wire2)

def checkForIntersection(seg1, seg2):
    (x1, y1), (x2, y2) = seg1 
    (x3, y3), (x4, y4) = seg2

    if (x2 - x1) == 0:
        seg1_vertical = True
    else:
        seg1_vertical = False
        
    if (x4 - x3) == 0:
        seg2_vertical = True
    else:
        seg2_vertical = False

    # Can't intersect if both segments have same orientation
    if seg1_vertical == seg2_vertical:
        return None

    if seg1_vertical:
        # seg1 is vertical with x1 == x2
        # seg2 is horizontal with y3 == y4
        if min(y1, y2) <= y3 and max(y1, y2) >= y3 and \
           min(x3, x4) <= x1 and max(x3, x4) >= x1:
            return (x1, y3)
        else:
            return None
    else:
        # seg1 is horizontal with y1 == y2
        # seg2 is vertical with x3 == x4
        if min(x1, x2) <= x3 and max(x1, x2) >= x3 and \
           min(y3, y4) <= y1 and max(y3, y4) >= y1:
            return (x3, y1)
        else:
            return None

def dist(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2

    return abs((x2 - x1)) + abs((y2 - y1))



best_intersect = float('infinity')
w1_steps = 0 # Steps so far for segment1
for w1_segment in zip(wire1_path[0:], wire1_path[1:]):
    w2_steps = 0
    for w2_segment in zip(wire2_path[0:], wire2_path[1:]):
        # Check for intersection
        res = checkForIntersection(w1_segment, w2_segment)

        if res is not None:
            steps_to_intersect = w1_steps + \
                                 w2_steps + \
                                 dist(w1_segment[0], res) + \
                                 dist(w2_segment[0], res)
            if steps_to_intersect < best_intersect and \
               steps_to_intersect > 0:
                best_intersect = steps_to_intersect
                coords = res

        w2_steps += dist(w2_segment[0], w2_segment[1])

    w1_steps += dist(w1_segment[0], w1_segment[1]) 

print(f"Best intersection at {coords} with {best_intersect} steps.")
