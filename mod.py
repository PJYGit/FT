# --------------------------
# CP460 (Fall 2019)
# Final Exam
# Jiayao Pang
# 194174300
# --------------------------

# Put your mod.py implementation here

import math
import string


# -----------------------------------------------------------
# Parameters:   mod (a positive integer)
# Return:       residueSet (list)
# Description:  Returns set of numbers in the given mod
#               which are residues of all other numbers
# Example:      residueSet for mod 5 --> [0,1,2,3,4]
# Errors:       mod has to be positive integer
#               return 'Error (residue_set): Invalid mod'
# -----------------------------------------------------------
def residue_set(mod):
    # your code here
    if not isinstance(mod, int) or int(mod) <= 0:
        return 'Error (residue_set): Invalid mod'

    residueSet = []
    for i in range(int(mod)):
        residueSet.append(i)

    return residueSet


# -----------------------------------------------------------
# Parameters:   num (any integer)
#               mod (a positive integer)
# Return:       residue
# Description:  Returns the smallest poisitive integer that is
#               congruent to num mod m
# Example:      residue 16 mod 5 --> 1
# Errors:       mod has to be positive integer
#                   return 'Error (residue): Invalid mod'
#               num should be integer
#                   return 'Error (residue): Invalid num'
# -----------------------------------------------------------
def residue(num, mod):
    # your code here
    if not isinstance(mod, int) or int(mod) <= 0:
        return 'Error (residue): Invalid mod'
    if not isinstance(num, int):
        return 'Error (residue): Invalid num'

    q = math.floor(num / mod)
    r = num - q * mod

    return r


# -----------------------------------------------------------
# Parameters:   a (any integer)
#               b (any integer)
#               m (a positive integer)
# Return:       True/False
# Description:  Returns True if a is congruent b mod m
#               return False otherwise
# Example:      isCongruent(22,33,11) --> True
#               isCongruent(7,9,3) --> False
# Errors:       mod has to be positive integer
#                   return 'Error (is_congruent): Invalid mod'
#               a and b should be integer
#                   return 'Error (is_congruent): Invalid input num'
# -----------------------------------------------------------
def is_congruent(a, b, m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (is_congruent): Invalid mod'
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error (is_congruent): Invalid input num'

    if residue(a, m) == residue(b, m):
        return True

    return False


# -----------------------------------------------------------
# Parameters:   a (any integer)
#               b (any integer)
#               m (positive integer)
# Return:       result (integer)
# Description:  Returns (a + b) mod m
#               result is an integer in residueSet mod m
# Example:      11 + 3 mod 5 = 4
# Errors:       a and b should be integers
#                   return 'Error (add): Invalid input num'
#               m should be positive integer
#                   return 'Error (add): Invalid mod'
# -----------------------------------------------------------
def add(a, b, m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (add): Invalid mod'
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error (add): Invalid input num'

    return residue(a + b, m)


# -----------------------------------------------------------
# Parameters:   a (any integer)
#               b (any integer)
#               m (positive integer)
# Return:       result (integer)
# Description:  Returns (a - b) mod m
#               result is an integer in residueSet mod m
# Example:      11 - 2 mod 5 = 4
# Errors:       a and b should be integers
#                   return 'Error (sub): Invalid input num'
#               m should be positive integer
#                   return 'Error (sub): Invalid mod'
# -----------------------------------------------------------
def sub(a, b, m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (sub): Invalid mod'
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error (sub): Invalid input num'

    return residue(a - b, m)


# -----------------------------------------------------------
# Parameters:   a (any integer)
#               m (positive integer)
# Return:       result (integer)
# Description:  Returns additive inverse of a mod m
#               result is an integer in residueSet mod m
# Example:      additive inverse of 7 mod 5 is
# Errors:       a and b should be integers
#                   return 'Error (add_inv): Invalid input num'
#               m should be positive integer
#                   return 'Error (add_inv): Invalid mod'
# -----------------------------------------------------------
def add_inv(a, m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (add_inv): Invalid mod'
    if not isinstance(a, int):
        return 'Error (add_inv): Invalid input num'

    if residue(a, m) == 0:
        return 0
    return m - residue(a, m)


# -----------------------------------------------------------
# Parameters:   m (positive integer)
# Return:       table (2D List)
# Description:  Returns addition table mod m
#               element [r][c] represent r+c mod m
# Example:      add table for mod 2 --> [[0,1],[1,0]]
# Errors:       m should be positive integer
#                   return 'Error (add_table): Invalid mod'
# -----------------------------------------------------------
def add_table(m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (add_table): Invalid mod'

    A_table = []
    for i in range(m):
        row = []
        for j in range(m):
            row.append(residue(i + j, m))

        A_table.append(row)

    return A_table


# -----------------------------------------------------------
# Parameters:   m (positive integer)
# Return:       table (2D List)
# Description:  Returns subtraction table mod m
#               element [r][c] represent r-c mod m
# Example:      subtraction table for mod 3 --> [[0,2,1],[1,0,2],[2,1,0]]
# Errors:       m should be positive integer
#                   return 'Error (sub_table): Invalid mod'
# -----------------------------------------------------------
def sub_table(m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (sub_table): Invalid mod'

    S_table = []
    for i in range(m):
        row = []
        for j in range(m):
            row.append(residue(i - j, m))

        S_table.append(row)

    return S_table


# -----------------------------------------------------------
# Parameters:   m (positive integer)
# Return:       table (2D List)
# Description:  Returns additive Inverse table mode m
#               Top row is num, bottom row is additive inverse
# Example:      Additive Inverse table mod 5 --> [[0,1,2,3,4],[0,4,3,2,1]]
# Errors:       m should be positive integer
#                   return 'Error (add_inv_table): Invalid mod'
# -----------------------------------------------------------
def add_inv_table(m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (add_inv_table): Invalid mod'

    r_set = residue_set(m)

    A_I_table = []
    A_I_table.append(r_set)

    temp = []
    for i in r_set:
        temp.append(add_inv(i, m))
    A_I_table.append(temp)

    return A_I_table


# -----------------------------------------------------------
# Parameters:   a (any integer)
#               b (any integer)
#               m (positive integer)
# Return:       result (integer)
# Description:  Returns (a * b) mod m
#               result is an integer in residueSet mod m
# Example:      11 * 2 mod 5 = 2
# Errors:       a and b should be integers
#                   return 'Error (mul): Invalid input num'
#               m should be positive integer
#                   return 'Error (mul): Invalid mod'
# -----------------------------------------------------------
def mul(a, b, m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (mul): Invalid mod'
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error (mul): Invalid input num'

    return residue(a * b, m)


# -----------------------------------------------------------
# Parameters:   m (positive integer)
# Return:       table (2D List)
# Description:  Returns multiplication table mod m
#               element [r][c] represent r*c mod m
# Example:      mul table for mod 4 -->
#                       [0, 0, 0, 0]
#                       [0, 1, 2, 3]
#                       [0, 2, 0, 2]
#                       [0, 3, 2, 1]
# Errors:       m should be positive integer
#                   return 'Error (mul_table): Invalid mod'
# -----------------------------------------------------------
def mul_table(m):
    # your code here
    if not isinstance(m, int) or int(m) <= 0:
        return 'Error (mul_table): Invalid mod'

    M_table = []
    for i in range(m):
        row = []
        for j in range(m):
            row.append(residue(i * j, m))

        M_table.append(row)

    return M_table


# -----------------------------------------------------------
# Parameters:   n (an integer)
# Return:       True/False
# Description:  Returns True if n is a prime
#               False otherwise
# Errors        None
# -----------------------------------------------------------
def is_prime(n):
    # your code here
    if n <= 3:
        return n > 1

    # all primes are equal to 6x + 1 or 6x + 5
    if n % 6 != 1 and n % 6 != 5:
        return False

    sq_root = int(math.sqrt(n))
    for i in range(5, sq_root + 1):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True


# -----------------------------------------------------------
# Parameters:   a (an integer)
#               b (an integer)
# Return:       gcd of a and b (int)
# Description:  Returns greatest common divider using standard
#               Euclidean Algorithm
#               Implementation can be recursive or iterative
# Errors:       a and b should be positive integers
#                   return 'Error (gcd): Invalid input value'
# -----------------------------------------------------------
def gcd(a, b):
    # your code here
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error (gcd): Invalid input value'
    if a == 0 or b == 0:
        return 'Error (gcd): Invalid input value'
    a = abs(a)
    b = abs(b)
    new_a = max(a, b)
    new_b = min(a, b)

    while (new_b != 0):
        temp = new_a
        new_a = new_b
        new_b = residue(temp, new_b)

    return new_a


# -----------------------------------------------------------
# Parameters:   a (an integer)
#               b (an integer)
# Return:       True/False
# Description:  Checks if two numbers are relatively prime
#               which is when gcd(a,b) equals 1
# Errors:       a and b should be integers
#                   return 'Error(is_relatively_prime): Invalid input num'
# -----------------------------------------------------------
def is_relatively_prime(a, b):
    # your code here
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error(is_relatively_prime): Invalid input num'

    if gcd(a, b) == 1:
        return True
    return False


# -----------------------------------------------------------
# Parameters:   a (an integer)
#               m (a positive integer)
# Return:       True/False
# Description:  Checks if number 'a' has a multiplicative inverse
#               in mod m. Returns True if such number exist
#               Returns False otherwise
# Errors:       a should be an integer
#                   return 'Error (has_mul_inv)" Invalid input num'
#               m should be a positive integer
#                   return 'Error (has_mul_inv): Invalid mod'
# -----------------------------------------------------------
def has_mul_inv(a, m):
    # your code here
    if not isinstance(a, int):
        return 'Error (has_mul_inv)" Invalid input num'
    if not isinstance(m, int) or m <= 0:
        return 'Error (has_mul_inv): Invalid mod'

    if gcd(a, m) == 1:
        return True
    return False


# -----------------------------------------------------------
# Parameters:   a (an integer)
#               b (an integer)
# Return:       [gcd(a,b) , s , t]
# Description:  Uses Extended Euclidean Algorithm to find
#               gcd of (a,b) but also numbers s and t such that
#               as + bt = gcd(a,b)
# Errors:       a and b should be integers not equal to 0
#                   return 'Error(eea): Invalid input num'
# -----------------------------------------------------------
def eea(a, b):
    # your code here
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error(eea): Invalid input num'
    if a == 0 or b == 0:
        return 'Error(eea): Invalid input num'

    u = [abs(a), 1, 0]
    v = [abs(b), 0, 1]
    r = []

    while v[0] != 0:
        q = math.floor(u[0] / v[0])
        r = [u[0] - q * v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u = v
        v = r

    return u


# -----------------------------------------------------------
# Parameters:   a (an integer)
#               m (positive integer)
# Return:       multiplicative inverse of a mod m
# Description:  Computes multiplicative inverse of 'a' mod m
#               If such number does not exist, the function
#               return 'NA'
# Errors:       a should be an integers
#                   return 'Error (mul_inv)" Invalid input num'
#               m should be a positive integer
#                   return 'Error (mul_inv): Invalid mod
# -----------------------------------------------------------
def mul_inv(a, m):
    # your code here
    if not isinstance(a, int):
        return 'Error (mul_inv)" Invalid input num'
    if not isinstance(m, int) or m <= 0:
        return 'Error (mul_inv): Invalid mod'
    if not has_mul_inv(a, m):
        return 'NA'

    u = eea(m, residue(a, m))

    return residue(u[2], m)


# -----------------------------------------------------------
# Parameters:   m (positive integer)
# Return:       table [2D list]
# Description:  Returns multiplicative Inverse table mode m
#               Top row is num, bottom row is multiplicative inverse
# Example:      Multiplicative Inverse table mod 5 -->
#                   [[0,1,2,3,4],['NA',1,3,2,4]]
# Errors:       m should be positive integer
#                   return 'Error (mul_inv_table): Invalid mod'
# -----------------------------------------------------------
def mul_inv_table(m):
    # your code here
    if not isinstance(m, int) or m <= 0:
        return 'Error (mul_inv_table): Invalid mod'

    re_set = residue_set(m)

    M_I_table = []
    M_I_table.append(re_set)

    temp = []
    for i in range(m):
        temp.append(mul_inv(i, m))
    M_I_table.append(temp)

    return M_I_table