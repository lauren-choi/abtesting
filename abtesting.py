from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2

import math

from abtesting_test import *

# You can comment out these lines! They are just here to help follow along to the tutorial.
print(t_dist.cdf(-2, 20)) # should print .02963
print(t_dist.cdf(2, 20)) # positive t-score (bad), should print .97036 (= 1 - .2963)

print(chi2.cdf(23.6, 12)) # prints 0.976
print(1 - chi2.cdf(23.6, 12)) # prints 1 - 0.976 = 0.023 (yay!)

# TODO: Fill in the following functions! Be sure to delete "pass" when you want to use/run a function!
# NOTE: You should not be using any outside libraries or functions other than the simple operators (+, **, etc)
# and the specifically mentioned functions (i.e. round, cdf functions...)

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
    '''
    Splices a the 2D list via start_row:end_row and start_col:end_col
    :param list: list of list of numbers
    :param nums: start_row, end_row, start_col, end_col
    :return: the spliced 2D list (ending indices are exclsive)
    '''
    to_append = []
    for l in range(start_row, end_row):
        to_append.append(list_2D[l][start_col:end_col])

    return to_append

def get_avg(nums):
    '''
    Helper function for calculating the average of a sample.
    :param nums: list of numbers
    :return: average of list
    '''
    sum = 0 
    for i in range(len(nums)):
        sum += nums[i]
    return sum / len(nums)

def get_stdev(nums):
    '''
    Helper function for calculating the standard deviation of a sample.
    :param nums: list of numbers
    :return: standard deviation of list
    '''
    sum = 0
    avg = get_avg(nums)
    for i in range(len(nums)):
        sum += (nums[i] - avg) ** 2
    stdev = (sum / (len(nums) - 1)) ** 0.5
    return stdev

def get_standard_error(a, b):
    '''
    Helper function for calculating the standard error, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: standard error of a and b (see studio 6 guide for this equation!)
    '''
    err_a = (get_stdev(a) ** 2) / len(a)
    err_b = (get_stdev(b) ** 2) / len(b)
    sterr = (err_a + err_b) ** 0.5
    return sterr

def get_2_sample_df(a, b):
    '''
    Calculates the combined degrees of freedom between two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
    HINT: you can use Math.round() to help you round!
    '''
    sterr = get_standard_error(a, b)
    denom_a = (((get_stdev(a) ** 2) / len(a)) ** 2) / (len(a) - 1)
    denom_b = (((get_stdev(b) ** 2) / len(b)) ** 2) / (len(b) - 1)
    df = round((sterr ** 4) / (denom_a + denom_b))
    return df

def get_t_score(a, b):
    '''
    Calculates the t-score, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
    '''
    avg_a = get_avg(a)
    avg_b = get_avg(b)
    se = get_standard_error(a, b)
    t_score = (avg_a - avg_b) / se
    return t_score

def perform_2_sample_t_test(a, b):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
    :param a: list of numbers
    :param b: list of numbers
    :return: calculated p-value
    HINT: the t_dist.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    t_score = get_t_score(a, b)
    df = get_2_sample_df(a, b)
    if (t_score > 0):
        t_score *= -1
    p = t_dist.cdf(t_score, df)
    return p


# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
def row_sum(observed_grid, ele_row):
    curr_row = observed_grid[ele_row]
    sum = 0
    for i in range(len(curr_row)):
        sum += curr_row[i]
    return sum

def col_sum(observed_grid, ele_col):
    num_rows = len(observed_grid)
    sum = 0
    for i in range(num_rows):
        sum += observed_grid[i][ele_col]
    return sum

def total_sum(observed_grid):
    num_cols = len(observed_grid[0])
    sum = 0
    for row in range(len(observed_grid)):
        for col in range(num_cols):
            sum += observed_grid[row][col]
    return sum

def calculate_expected(row_sum, col_sum, tot_sum):
    expected = (row_sum * col_sum) / tot_sum
    return expected

def get_expected_grid(observed_grid):
    '''
    Calculates the expected counts, given the observed counts.
    ** DO NOT modify the parameter, observed_grid. **
    :param observed_grid: 2D list of observed counts
    :return: 2D list of expected counts
    HINT: To clean up this calculation, consider filling in the optional helper functions below!
    '''
    #TODO: fill me in!
    row = len(observed_grid)
    col = len(observed_grid[0])
    expected = []
    total = total_sum(observed_grid)
    for r in range(row):
        new_row = []
        for c in range(col):
            row_total = row_sum(observed_grid, r)
            col_total = col_sum(observed_grid, c)
            new_row.append(calculate_expected(row_total, col_total, total))
        expected.append(new_row)
    return expected

def df_chi2(observed_grid):
    '''
    Calculates the degrees of freedom of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    rows = len(observed_grid)
    cols = len(observed_grid[0])
    df = (rows - 1) * (cols - 1)
    return df

def chi2_value(observed_grid):
    '''
    Calculates the chi^2 value of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    expected_grid = get_expected_grid(observed_grid)
    overall_value = 0
    num_cols = len(observed_grid[0])
    for row in range(len(observed_grid)):
        for col in range(num_cols):
            observed = observed_grid[row][col]
            expected = expected_grid[row][col]
            overall_value += ((observed - expected) ** 2) / expected
    return overall_value

def perform_chi2_homogeneity_test(observed_grid):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates the p-value by performing a chi^2 test, given a list of observed counts
    :param observed_grid: 2D list of observed counts
    :return: calculated p-value
    HINT: the chi2.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    chi2_val = chi2_value(observed_grid)
    df = df_chi2(observed_grid)
    area = chi2.cdf(chi2_val, df)
    chi2_test = 1 - area
    return chi2_test

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
    Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
    This will be useful when you need to run your tests on your cleaned log data!
    :param str: string holding data
    :return: the spliced list of numbers
    '''
  return list(map(float, s.split()))


# t_test 1:
a_t1_list = data_to_num_list(a1) 
b_t1_list = data_to_num_list(b1)
print(get_t_score(a_t1_list, b_t1_list)) # this should be -129.500
print(perform_2_sample_t_test(a_t1_list, b_t1_list)) # this should be 0.0000
# why do you think this is? Take a peek at a1 and b1 in abtesting_test.py :)

# t_test 2:
a_t2_list = data_to_num_list(a2) 
b_t2_list = data_to_num_list(b2)
print(get_t_score(a_t2_list, b_t2_list)) # this should be -1.48834
print(perform_2_sample_t_test(a_t2_list, b_t2_list)) # this should be .082379

# t_test 3:
a_t3_list = data_to_num_list(a3) 
b_t3_list = data_to_num_list(b3)
print(get_t_score(a_t3_list, b_t3_list)) # this should be -2.88969
print(perform_2_sample_t_test(a_t3_list, b_t3_list)) # this should be .005091
"""

"""
# chi2_test 1:
a_c1_list = data_to_num_list(a_count_1) 
b_c1_list = data_to_num_list(b_count_1)
c1_observed_grid = [a_c1_list, b_c1_list]
print(chi2_value(c1_observed_grid)) # this should be 4.103536
print(perform_chi2_homogeneity_test(c1_observed_grid)) # this should be .0427939

# chi2_test 2:
a_c2_list = data_to_num_list(a_count_2) 
b_c2_list = data_to_num_list(b_count_2)
c2_observed_grid = [a_c2_list, b_c2_list]
print(chi2_value(c2_observed_grid)) # this should be 33.86444
print(perform_chi2_homogeneity_test(c2_observed_grid)) # this should be 0.0000
# Again, why do you think this is? Take a peek at a_count_2 and b_count_2 in abtesting_test.py :)

# chi2_test 3:
a_c3_list = data_to_num_list(a_count_3) 
b_c3_list = data_to_num_list(b_count_3)
c3_observed_grid = [a_c3_list, b_c3_list]
print(chi2_value(c3_observed_grid)) # this should be .3119402
print(perform_chi2_homogeneity_test(c3_observed_grid)) # this should be .57649202