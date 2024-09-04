# Red Black Tree

class RBNode:
    def __init__(self, key, color):
        self.key = key # Node's value/key, ex; 24 or 543
        self.right = None # Right child
        self.left = None # Left child
        self.parent = None # Node's parent
        self.color = color # 0 is Red, 1 is Black

class RBTree:
    def __init__(self, z):
        self.root = z
        self.nil = RBNode(None, 1)

    def leftRotate(self, x):
        y = x.right
        x.right = y.left # Turn y's L subtree into x's R subtree
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent # Link x parent to y parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left: # Is x the left or right child
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right # Turn y's R subtree into x's L subtree
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent # Link x parent to y parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right: # Is x the left or right child
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insertFix(self, z):
        while z.parent.color == 0:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                
                if y.color == 0: # Case 1
                    z.parent.color = 1
                    y.color = 1
                    z.parent.parent.color = 0
                    z = z.parent.parent
                    
                else:
                    if z == z.parent.right: # Case 2
                        z = z.parent
                        self.leftRotate(z)

                    z.parent.color = 1 # Case 3
                    z.parent.parent.color = 0
                    self.rightRotate(z.parent.parent)
                
            else: # Flip left and right's if z.p is not z.p.p.l
                y = z.parent.parent.left

                if y.color == 0:
                    z.parent.color = 1
                    y.color = 1
                    z.parent.parent.color = 0
                    z = z.parent.parent
                    
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rightRotate(z)

                    z.parent.color = 1
                    z.parent.parent.color = 0
                    self.leftRotate(z.parent.parent)

        self.root.color = 1
                

    def insert(self, z):
        y = self.nil

        if self.root == None:
            self.root = self.nil
        x = self.root

        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key: # Determine if z is L or R child
            y.left = z
        else:
            y.right = z

        z.left = self.nil
        z.right = self.nil
        z.color = 0        
        self.insertFix(z)

    def search(self, k):
        if self.root == None or k == self.root.key: # Check if k is equal to root key
            return self.root                        # Or if tree exists
        elif k < self.root.key: # If k less than root key, search left branch
            return RBTree(self.root.left).search(k)
        elif k > self.root.key: # Else search right branch for k
            return RBTree(self.root.right).search(k)
        else:
            return RBNode(-1) # Return -1 if the searched key is not present

    def treeMin(self, y):
        x = y
        while x.left != self.nil:
            x = x.left
        return x

    def transplant(self, u, v):
        if u.parent == self.nil: # Ensure existance
            self.root = v
        elif u == u.parent.left: # Determine if left or right child
            u.parent.left = v
        else:
            u.parent.right = v
   
        v.parent = u.parent

    def deleteFixup(self, x):
        while x != self.root and x.color == 1:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 0: # Case 1
                    w.color = 1
                    x.parent.color = 0
                    self.leftRotate(x.parent)
                    w = x.parent.right
                    
                if w.left.color == 1 and w.right.color == 1: # Case 2
                    w.color = 0
                    x = x.parent
                else:
                    if w.right.color == 1: # Case 3
                        w.left.color = 1
                        w.color = 0
                        self.rightRotate(w)
                        w = x.parent.right

                    w.color = x.parent.color # Case 4
                    x.parent.color = 1
                    w.right.color = 1
                    self.leftRotate(x.parent)
                    x = self.root
            else: # Flip lefts and rights if x is not left child
                w = x.parent.left
                if w.color == 0:
                    w.color = 1
                    x.parent.color = 0
                    self.rightRotate(x.parent)
                    w = x.parent.left
                    
                if w.right.color == 1 and w.left.color == 1:
                    w.color = 0
                    x = x.parent
                else:
                    if w.left.color == 1:
                        w.right.color = 1
                        w.color = 0
                        self.leftRotate(w)
                        w = x.parent.left
            
                    w.color = x.parent.color
                    x.parent.color = 1
                    w.left.color = 1
                    self.rightRotate(x.parent)
                    x = self.root

        x.color = 1

    def delete(self, z):
        y = z
        y_ogColor = y.color
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.treeMin(z.right)
            y_ogColor = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if y_ogColor == 1:
            self.deleteFixup(x)

    def countup(self, z): # Simple counter to tally black nodes
        count = 0
        x = z

        while x != self.root: # Countinue looping until root is reached
            if x.color == 1:
                count += 1
            x = x.parent

        return count + 1

    def findLeaves(self):
        curr = self.root
        stack = []
        leaves = []
        while True: # AKA until else is entered
            if curr != self.nil:
                stack.append(curr)
                curr = curr.left
            elif(stack):
                curr = stack.pop()
                if curr.left == self.nil and curr.right == self.nil:
                    leaves.append(curr)
                curr = curr.right
            else:
                return leaves

    def verify(self):
        leaves = self.findLeaves()
        counts = []
        while(leaves):
            x = leaves.pop()
            counts.append(self.countup(x))
        print("\n", counts) # Prints the array for a visual rep of what each root->leaf's B count is
        verified = True
        for i in range(len(counts)-1):
            if counts[i] != counts[i+1]:
                verified = False

        if(verified):
            print("RB Tree has been verified.")
        else:
            print("RB Tree failed verification")

    def height(self):
        if self.root == None:
            return 0

        leftCnt = RBTree(self.root.left).height()
        rightCnt = RBTree(self.root.right).height()
        return max(leftCnt, rightCnt) + 1

    def inorder(self):
        if self.root.key != None:
            RBTree(self.root.left).inorder()
            #print(self.root.key, " - ", self.root.color) 
            print(self.root.key)
            RBTree(self.root.right).inorder()
