import numpy as np
with open("input2.txt", "r") as f:
    data = [orbit.strip("\n") for orbit in f.readlines()]

#data = ["COM)B",
#        "B)C",
#        "C)D",
#        "D)E",
#        "E)F",
#        "B)G",
#        "G)H",
#        "D)I",
#        "E)J",
#        "J)K",
#        "K)L"]

#data = ["A)B", "COM)D", "B)C", "D)A"]
#data = ["COM)A", "A)B", "B)C", "C)E", "F)E"]
#data = ["E)J", "F)E", "COM)F"]

class Node:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.children = []
        self.dist = float('infinity')
        self.length = 1
        self.goes_to = None

def searchNode(node, targetVal):
    if node.val == targetVal:
        return node
    else:
        for c in node.children:
            found = searchNode(c, targetVal)
            if found:
                return found

        # Could not find node
        return None

def searchNode2(node, targetVal, depth):
    if node.val == targetVal:
        return node
    else:
        for c in node.children:
            found, depth = searchNode2(c, targetVal, depth+1)
            if found:
                return found, depth

        # Could not find node
        return None, None

def printTree(node, depth, depthMax):
    if depth == depthMax:
        return

    val = node.val
    children_vals = [n.val for n in node.children]
    print(f"[{val}]: {children_vals}", sep="")
    for child in node.children:
        printTree(child, depth+1, depthMax)

# For every node, accumulate the number of steps taken to get there
def countOrbits(node, depth, accum):
    if node.children == []:
        return accum
    else:
        res = 0
        for c in node.children:
            res += 1 + countOrbits(c, depth+1, accum) + depth

        return res 

# Initialize tree pre-loop
root = Node("root")
for o in data[0:]:
    parent_val, child_val = o.split(')')
    print(f"Got {parent_val} - {child_val}")

    # Find if parent exists in tree
    pTree = searchNode(root, parent_val)
    # Find if child exists in tree
    cTree = searchNode(root, child_val)

    # Both exist in tree
    if pTree is not None and cTree is not None:
        print(f"Found parent and child in tree. Linking")
        cTree.parent.children.remove(cTree)
        pTree.children.append(cTree)
        cTree.parent = pTree
    # Child doesn't exist
    elif pTree is not None:
        # Create new node for child
        print(f"Coulnd't find child. Creating to parent {parent_val}.")
        child = Node(child_val)
        child.parent = pTree
        pTree.children.append(child)
    # Parent doesn't exist
    elif cTree is not None:
        print(f"Coulnd't find parent. Creating parent {parent_val} to child {child_val}.")
        # Create new node for parent
        parent = Node(parent_val)
        parent.children.append(cTree)
        # Connect to root 
        parent.parent = root
        # If child of this parent was a child of root remove it
        root.children.remove(cTree)
        root.children.append(parent)
        # Connect child to newly created parent
        cTree.parent = parent

    # Both don't exist in tree
    else:
        print(f"Couldn't find parent and child in tree.")
        # Create new node for both and append to root
        parent = Node(parent_val)
        parent.parent = root
        child = Node(child_val)
        child.parent = parent
        parent.children.append(child)
        root.children.append(parent)

# bye bye "root"

#printTree(root, 0, 100)
#res = countOrbits(root.children[0], 0, 0)

# Find YOU
you_node = searchNode(root, "YOU")
san_node = searchNode(root, "SAN")
root.children[0].parent = None
print(root.children[0].val)
print(root.children[0].parent)
print(root.parent)

# Find the shortest path going "up"
visited = []
unvisited = [you_node]
cNode = you_node
cNode.dist = 0
count = 0
while len(unvisited) != 0:
    #print(f"cNode: {cNode.val}.")
    # Newly seen node
    neighbors = []
    if cNode.parent != None and cNode.parent.val == "root":
        print(f"{cNode.val} my parent is root ..")

    if cNode.parent not in visited and cNode.parent not in unvisited and \
            cNode.parent is not None:
        unvisited.append(cNode.parent)
        neighbors.append(cNode.parent)
    elif cNode.parent not in visited and cNode.parent is not None:
        neighbors.append(cNode.parent)

    for child in cNode.children:
        if child.val == "root":
            print("child is root...")
        if child not in visited and child not in unvisited:
            unvisited.append(child)
            neighbors.append(child)
        elif child not in visited:
            neighbors.append(child)

    n_vals = [n.val for n in neighbors]
    #print(f"Neighbors: {n_vals}.")

    for neighbor in neighbors:
        dist = cNode.dist + neighbor.length
        if dist < neighbor.dist:
            neighbor.dist = dist
            neighbor.goes_to = cNode

    visited.append(cNode)
    unvisited.remove(cNode)

    smallest_dist = float('inf')
    for node in unvisited:
        if node.dist < smallest_dist:
            cNode = node
            smallest_dist = node.dist

n = san_node
while n != None:
    print(f"{n.val}: {n.dist}")
    n = n.goes_to

print(f"Smallest distance: {san_node.dist}.")
