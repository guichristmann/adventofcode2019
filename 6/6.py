import numpy as np
with open("input.txt", "r") as f:
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

def updateRootNode(node):
    if node.parent == None:
        return node
    else:
        return updateRootNode(node.parent)
        
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

printTree(root, 0, 100)
res = countOrbits(root.children[0], 0, 0)
print(res)
