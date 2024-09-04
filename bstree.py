# Binary Search Tree

class BSNode:
    def __init__(self, key):
        self.key = key # Node's value/key, ex; 24 or 543
        self.right = None # Right child
        self.left = None # Left child
        self.parent = None # Node's parent

# BSTree declaration including all related code (insert, delete, etc)
class BSTree:
    def __init__(self, z):
        self.root = z
        self.size = 0

    # BS Tree insert
    def insert(self, z):
        y = None
        x = self.root
        
        while x != None:
            y = x
            if z.key < x.key: # Traverse Left
                x = x.left
            else: # Traverse Right
                x = x.right

        z.parent = y
        if y == None: # Tree is empty
            self.root = z
        elif z.key < y.key:
            y.left = z # z is left child
            z.parent = y
        else:
            y.right = z # z is right child
            z.parent = y

    # In-order traversal from least key value to highest key value
    def inorder(self):
        if self.root:
            BSTree(self.root.left).inorder()
            print(self.root.key)
            BSTree(self.root.right).inorder()

    # BS Tree search for a given key value
    def search(self, k):
        if self.root == None or k == self.root.key: # Check if k is equal to root key
            return self.root                        # Or if tree exists
        elif k < self.root.key: # If k less than root key, search left branch
            return BSTree(self.root.left).search(k)
        elif k > self.root.key: # Else search right branch for k
            return BSTree(self.root.right).search(k)
        else:
            return BSNode(-1) # Return -1 if the searched key is not present

    def treeMin(self, y):
        x = y
        while x.left != None:
            x = x.left
        return x

    def transplant(self, u, v):
        if u.parent == None: # Ensure parent exists
            self.root = v
        elif u == u.parent.left: # Determine if left or right child
            u.parent.left = v
        else:
            u.parent.right = v

        if v != None:
            v.parent = u.parent
            
    def delete(self, z):
        if z.left == None:              # Case 1 and half of Case 2
            self.transplant(z, z.right)
        elif z.right == None:           # Second half of Case 2
            self.transplant(z, z.left)
        else:
            y = self.treeMin(z.right) # Find successor
            if y.parent != z: # Half of case 3.2
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                
            self.transplant(z, y) # Case 3.1 and other half of 3.2
            y.left = z.left
            y.left.parent = y

    def height(self):
        if self.root == None: # If there is no root node, then height is 0
            return 0
        else: # Take the highest count from the left or right side
            leftCnt = BSTree(self.root.left).height()
            rightCnt = BSTree(self.root.right).height()
            return max(leftCnt, rightCnt) + 1
