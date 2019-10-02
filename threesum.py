# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:53:40 2019

@author: Nathan Brooks
"""

MIN_BASE = 4
MAX_BASE = 9
EXPERIMENTS = 100

"""
brute-force solution for three sum
returns the sum of all unique combinations that sum to 0
It will still be O(n^3)
"""
def ThreeSumBruteForce(array: list) -> int: 
    from itertools import combinations
    return sum([not sum(i) for i in combinations(array, 3)])


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


"""
verifies a few test cases render correct results
"""
def VerifyThreeSum():
    # group is [-12, 8, 4]
    array = [1, 4, 45, 6, -12, 8]
    assert 1 == ThreeSumBruteForce(array)
    assert 1 == ThreeSumFast(array)
    assert 1 == ThreeSumFastest(array)
    
    # groups are [0,0,0], [0,0,0], [0,0,0], [0,0,0]
    # this is each combination of 0s
    array = [0, 0, 0, 0]
    assert 4 == ThreeSumBruteForce(array)
    assert 4 == ThreeSumFast(array)
    assert 4 == ThreeSumFastest(array)    
    
    # groups are [-1,0,1] and [2,1,-3]
    array = [0, -1, 2, -3, 1]
    assert 2 == ThreeSumBruteForce(array)
    assert 2 == ThreeSumFast(array)
    assert 2 == ThreeSumFastest(array)

    # does not hit this if any previous failed
    print('All test cases passed')


"""
this is the experiment and graphing of the experiment
"""
if __name__ == '__main__':
    from random import choices
    from stopwatch import stopwatch
    from tqdm import trange
    import pandas as pd
    import math
    from scipy.optimize import minimize
    import matplotlib.pyplot as plt
    
    # timekeeping and dataframe for keeping track of records
    clock = stopwatch()
    times = pd.DataFrame(columns=list(zip(['ThreeSumBruteForce',\
        'ThreeSumFast', 'ThreeSumFastest'], ['total']*3)))
    
    # each order of magnitude (base 2) in range
    for i in trange(MIN_BASE, MAX_BASE, desc='Each Base:'):
        # set i, create array of numbers, make record
        i = 2**i
        row = pd.Series(name=i, index=times.columns, data=[0,0,0])
        
        # for each experiment type, make an array and run it through each
        for _ in trange(EXPERIMENTS, desc='n='+str(i)):
            brute_array = choices(range(-int(2e9), int(2e9)), k=i)
        
            # brute experiment
            clock.start()
            _ = ThreeSumBruteForce(brute_array)
            row[('ThreeSumBruteForce', 'total')] += clock.time()
            
            # fast experiment
            temp_array = brute_array.copy()
            clock.start()
            _ = ThreeSumFast(temp_array)
            row[('ThreeSumFast', 'total')] += clock.time()
            
            # fastest experiment
            temp_array = brute_array.copy()
            clock.start()
            _ = ThreeSumFastest(temp_array)
            row[('ThreeSumFastest', 'total')] += clock.time()
        
        # append record to table
        times = times.append(row)
    
    
    # analyzing the results (the index is n, the number of list items)
    # turn each column into its own dataframe. find average, find ratio
    for col in list(times):
        times[(col[0], 'avg')] = times[col].div(EXPERIMENTS)
        times[(col[0], 'ratio')] = times[col].pct_change().add(1)
    times.columns = pd.MultiIndex.from_tuples(times.columns,\
                                              names=['algorithm', 'metric'])
    
    # this is for table of averages
    # averages = times.xs('avg', level='metric', axis=1)
    # this is for table of ratios
    # ratios = times.xs('ratio', level='metric', axis=1)
    
    # this is where I fit the lines to the averages
    # here I create a least squares formula for cubic functions, minimize, and 
    # plot the results for the BruteFroceAlgorithm
    def cubic_fit(args):
        y, a = args
        total = 0
        for i, x in times[('ThreeSumBruteForce', 'avg')].iteritems():
            total += (x - y - a*i**3)**2
        return total
    
    ans = minimize(cubic_fit, [0,0], method='Nelder-Mead')
    times[('ThreeSumBruteForce', 'predict')] = times.index.map(lambda x:\
          ans.x[0]+ans.x[1]*x**3)
    # plot values and predicted values
    times['ThreeSumBruteForce'][['avg', 'predict']].plot(title=\
         'ThreeSumBruteForce')
    plt.show()
    
    # this is O(n^2log(n)) for the BruteForceFast
    # same idea for the regression, added abs for b to prevent domain errors
    def quad_log_fit(args):
        y, a, b = args
        b = max(0.000001, abs(b))
        total = 0
        for i, x in times[('ThreeSumFast', 'avg')].iteritems():
            total += (x - (y + a*(i**2)*math.log(i, b)))**2
        return total
    
    ans = minimize(quad_log_fit, [0,0,0], method='Nelder-Mead')
    y, a, b = ans.x
    b = max(0.000001, abs(b))
    times[('ThreeSumFast', 'predict')] = times.index.map(lambda x: (y +\
          a*(x**2)*math.log(x, b)))
    # plot values and predicted values
    times['ThreeSumFast'][['avg', 'predict']].plot(title='ThreeSumFast')
    plt.show()
    
    # this is O(n^2) for the BruteForceFastest
    # same idea for regression and plotting
    def quad_fit(args):
        y, a = args
        total = 0
        for i, x in times[('ThreeSumFastest', 'avg')].iteritems():
            total += (x - (y + a*(i**2)))**2
        return total
    
    ans = minimize(quad_fit, [0,0], method='Nelder-Mead')
    y, a = ans.x
    times[('ThreeSumFastest', 'predict')] = times.index.map(lambda x:\
          (y + a*(x**2)))
    # plot expected values and real values
    times['ThreeSumFastest'][['avg', 'predict']].plot(title='ThreeSumFastest')
    plt.show()

    # here is where  log-linear plots are printed
    times['ThreeSumBruteForce'][['avg', 'predict']].plot(title=\
         'ThreeSumBruteForce', logy=True)
    plt.show()
    times['ThreeSumFast'][['avg', 'predict']].plot(title='ThreeSumFast',\
         logy=True)
    plt.show()
    times['ThreeSumFastest'][['avg', 'predict']].plot(title='ThreeSumFastest',\
         logy=True)
    plt.show()


