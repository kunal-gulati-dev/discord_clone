Given a linked list A, remove the B-th node from the end of the list and return its head. for example, Given linked list: 1-> 2 -> 3-> 4 -> 5 and B = 2. After removing the second node from the end, the linked list becomes 1 -> 2 -> 3 -> 5. NOTE: if B is greater than the size of the list, remove the first node of the list. NOTE: try doing it using constant additonal space.


import heapq
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def removeNthFromEnd(self, A, B):

# Given the root of a binary search tree of size N with distinct values, transform it into "greater sum tree" such that each node in the new tree has a value equal to the original tree node vlaue plus the sum of all values greater than the original node value in the tree. Return the new binary search tree.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.sum = 0

    def bstToGst(self, root):
        if root:
            # Traverse the right subtree
            self.bstToGst(root.right)

            # Update the node value with the running sum
            self.sum += root.val
            root.val = self.sum

            # Traverse the left subtree
            self.bstToGst(root.left)

        return root


you are given an array of integers A of size N, where each element represents the weight of a stone. we are playing a game with the stones. On each turn, we choose the two heaviest stones and smash them together.
suppose the stones have weight x and y with x <= y. The result of this smash is:

if x == y, both stones are totally destroyed. 
if x != y, the stone of weight x is totally destroyed, and the stone of weight y has new weight y - x

At the end, there is at most one stone left. Return the weight of this stone (or 0 if there are no stones left)


import heapq

class Solution:
    def lastStoneWeight(self, stones):
        # Convert the array into a max heap (negate the values)
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)

        # Continue smashing stones until there's at most one stone left
        while len(max_heap) > 1:
            x = -heapq.heappop(max_heap)  # Get the heaviest stone
            y = -heapq.heappop(max_heap)  # Get the second heaviest stone

            if x != y:
                # If the stones have different weights, calculate the new weight
                new_weight = y - x
                heapq.heappush(max_heap, -new_weight)

        # Return the weight of the last stone (or 0 if no stones are left)
        return -max_heap[0] if max_heap else 0


# A : [70, 96, 76, 37, 72, 36, 69]

# -26
# 14


# Given a set of distinct integers A. return all possible subsets.

# Note:
    
# 1. Elements in a subset must be in non descending order.
# 2. The solution set must not contain duplicate subsets.
# 3. Also, the subsets should be sorted in ascending (lexicographic) order.   
# 4. The initial list is not necessary sorted.

# class Solution:
#     def subsets(self, A):


# solve in this format and in the most optimized way possible.



# Given a matrix of integers A of size N * M consisting of 0 and 1. A group of connected 1's forms an island. From a cell (i, j) such that A[i][j] = 1 you can visit any cell that shares a side with (i, j) and value in that cell is 1.
# More formally, from any cell (i, j) if A[i][j] = 1 you can visit.

# (i - 1, j) if (i - 1, j) is inside the matrix and A[i - 1][j] = 1.
# (i, j - 1) if (i, j - 1) is inside the matrix and A[i][j - 1] = 1.
# (i + 1, j) if (i + 1, j) is inside the matrix and A[i + 1][j] = 1.
# (i, j + 1) if (i, j + 1) is inside the matrix and A[i][j + 1] = 1.

# Return the number os island.

# Note:
# 1. Rows are numbered from top to bottom and columns are numbered from left to right.
# 2. Your solution will run on multiple test cases. If you are using global variables, make sure to clear them.

# class Solution:
#     def solve(self, A):


# solve in this format and in the most optimized way possible.


class Solution:
    def solve(self, A):
        if not A:
            return 0

        def dfs(i, j):
            if i < 0 or i >= len(A) or j < 0 or j >= len(A[0]) or A[i][j] == 0:
                return
            A[i][j] = 0  # Mark the cell as visited
            for dx, dy in directions:
                dfs(i + dx, j + dy)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        count = 0

        for i in range(len(A)):
            for j in range(len(A[0])):
                if A[i][j] == 1:
                    dfs(i, j)
                    count += 1

        return count


while fast.next is not None:

AttributeError: "NoneType" object has no attribute "next"