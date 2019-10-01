# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:53:40 2019

@author: Nathan Brooks
"""

# In[]

"""
brute-force solution for three sum
returns the sum of all unique combinations that sum to 0
It will still be O(n^3)
"""
def ThreeSumBruteForce(array: list) -> int: 
    from itertools import combinations
    return sum([not sum(i) for i in combinations(array, 3)])

# In[]

"""
three sum soltion which sorts array
goes through all combinations of two integers, checking if a third integer
exists in the array which allows the two sum to sum to 0. O(n^2log(n))
"""
def ThreeSumFast(array: list) -> int: 
    from itertools import combinations
    from bisect import bisect_left, bisect_right
    
    # sort and create counter for 0 sums
    array.sort()
    count = 0
    
    # get indexes and values for each pair of integers
    for (a_key, a_val), (b_key, b_val) in combinations(enumerate(array), 2):
        # find value that would allow this pair to sum to 0
        c_val = -(a_val + b_val)
        # find the maximum index not already taken and below c_val
        c_min = max(bisect_left(array, c_val), b_key + 1)
        # find the minimum index above c_val
        c_max = bisect_right(array, c_val, c_min, len(array))
        # add the difference between indexes
        count += c_max - c_min
    
    return count

# In[]

"""
three sum solution with hashmap
handles situation where 3 of three sum are equal, 2 of three sum are equal, 
and all of three sum are unique separatly. Worst case: O(n^2)
"""
def ThreeSumFastest(array: list) -> int: 
    from collections import defaultdict
    from bisect import bisect_left, bisect_right
    from math import factorial
    
    # naive case
    if len(array) < 3: return 0
    
    # count occurences of each
    c = defaultdict(int)
    for val in array:
        c[val] += 1
    
    # get unique items and create count to count 0 sums
    keys = sorted(c)
    count = 0
    
    # handle only solution(s) where a, b, c are equal
    # based on combinations = x! / (r! * (x-r)!) where r is size of reduction
    # and x is the size of the group
    if 0 in c:
        if c[0] >= 3:
            count += int(factorial(c[0]) / (6 * factorial(c[0] - 3)))
    
    # iterate through each unique item of array
    right = len(keys)
    for i, x in enumerate(keys):
        # handle situations where 2 values of sum are equal
        # find combinations of equal pair, multiply by count of single
        # make sure that x isn't 0 because 0s were covered in all equal case
        if x and c[x] >= 2 and -2 * x in c:
            pair = int((factorial(c[x]) >> 1) / factorial(c[x] - 2))
            count += pair * c[-2 * x]
        
        # only bother with negative values you can find a positive two sum
        # comlement for where all values of three sum are unique
        if x < 0:
            twosum = -x
            # smallest index of possible twosum component
            left = bisect_left(keys, twosum - keys[-1], lo=i+1, hi=right)
            # largest index of possible twosum component
            right = bisect_right(keys, twosum >> 1, lo=left)
            # where all are unqique, multiply counts for count of combinations
            for positive in keys[left:right]:
                other = twosum - positive
                if other in c and other != positive:
                    count += c[x] * c[other] * c[positive]
    
    return count












