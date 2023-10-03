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



contest 2


Given a set of N intervals denoted by 2D array A of size N * 2, the task is to find the length of maximal set of mutually disjoint intervals.

two intervals [x, y] and [p, q] are said to be disjoint if they do not have any point in common.

Return a integer denoting the length of maximal set of mutually disjoint intervals.


class Solution:
    def solve(self, A):
        if not A:
            return 0

        # Sort the intervals by their ending points
        A.sort(key=lambda interval: interval[1])

        count = 1  # Initialize count to 1 since the first interval is always selected
        end = A[0][1]

        for i in range(1, len(A)):
            if A[i][0] > end:  # If the interval doesn't overlap with the previous one
                count += 1
                end = A[i][1]

        return count


Thomas found an array A of length n representing some integer numbers. The array was initially sorted in ascending order. He kept the array and went to get some food, on returning he found his brother has rotated it by some amount between 1 and n.

For Example, the sorted array which Thomas had was A = [0,1,2, 4, 5, 6, 7], became:
    1. [4, 5, 6, 7, 0, 1, 2] if it was rotated 4 times.
    2. [0, 1, 2, 4, 5, 6, 7] if it was rotated 7 times.

Rotating an array [a[0], a[1], a[2], .....a[n - 1]] by one time shifts the elements in such a way that the result is the array [a[n - 1], a[0], a[1], a[2], ....a[n - 2]]

Given the sorted rotated array A of unique elements, return the minimum element of this array.

You must write an alogorithm that runs O(logn) times.


class Solution:
    def findMin(self, A):
        left, right = 0, len(A) - 1

        while left < right:
            mid = left + (right - left) // 2

            if A[mid] > A[right]:
                left = mid + 1
            else:
                right = mid

        return A[left]





Given a matrix of integers A of size N * M and an integer B.

In a given matrix every row and column is sorted in non decreasing order. Find and return the position of B in the matrix in the given form.
1. if A[i][j] = B then return (i * 1009 + j)
2.  If B is not present return -1

Note 1: Rows are numbered from top to bottom and columns are numbered from left to right.
Note 2: If there are multiple B in A then return the smallest value of i*1009 + j such that A[i][j] = B. 
Note 3: Expected time complexity is linear.
Note 4: Use 1-based indexing.


class Solution:
    def solve(self, A, B):
        n = len(A)
        m = len(A[0])
        i, j = 0, m - 1

        while i < n and j >= 0:
            if A[i][j] == B:
                return (i + 1) * 1009 + (j + 1)
            elif A[i][j] > B:
                j -= 1
            else:
                i += 1

        return -1





Say you have an array A, for which the ith element is the price of a given stock on day i.
If you were only permitted to complete at most one transaction (ie. buy one and sell one share of the stock), design an algorithm to find the maximum profit.
Return the maximum possible profit.


class Solution:
    def maxProfit(self, A):
        if not A:
            return 0

        min_price = A[0]  # Initialize the minimum price as the first element
        max_profit = 0  # Initialize the maximum profit as 0

        for price in A:
            # Update the minimum price if needed
            min_price = min(min_price, price)
            # Update the maximum profit
            max_profit = max(max_profit, price - min_price)

        return max_profit


Determine the "GOOD"ness of a given string A, where the "GOOD"ness is defined by the length of the longest substring that contains no repeating characters. the greater the length of this unique-character substring, the higher the "GOOD"ness of the string.

Your task is to return an integer representing the "GOOD"ness of string A. 

Note: The solution should be achieved in O(N) time complexity, where N is the length of the string.


class Solution:
    def lengthOfLongestSubstring(self, A):
        n = len(A)
        if n <= 1:
            return n

        char_index = {}  # Dictionary to store the last seen index of each character
        max_length = 0  # Initialize the maximum substring length
        start = 0  # Initialize the start of the sliding window

        for end in range(n):
            if A[end] in char_index and char_index[A[end]] >= start:
                # If the character is already in the current substring, update the start
                start = char_index[A[end]] + 1
            # Update the last seen index of the character
            char_index[A[end]] = end
            # Update the maximum length
            max_length = max(max_length, end - start + 1)

        return max_length





































































