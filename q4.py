# --------------------------
# CP460 (Fall 2019)
# Final Exam
# Jiayao Pang
# 194174300
# --------------------------

import math
import string
import mod
import SDES
import utilities
import matrix


# add functions related to q4 here
# ----------------------------------------------------
# Parameters:   None
# Return:       polybius_square (string)
# Description:  Returns the following polybius square
#               as a sequential string:
#               [1] [2]  [3] [4] [5] [6] [7] [8]
#           [1]      !    "   #   $   %   &   '
#           [2]  (   )    *   +   '   -   .   /
#           [3]  0   1    2   3   4   5   6   7
#           [4]  8   9    :   ;   <   =   >   ?
#           [5]  @   A    B   C   D   E   F   G
#           [6]  H   I    J   K   L   M   N   O
#           [7]  P   Q    R   S   T   U   V   W
#           [8]  X   Y    Z   [   \   ]   ^   _
# ---------------------------------------------------
def get_polybius_square():
    polybius_square = ''
    # your code here
    # use the chr() function is easier
    for i in range(32, 96):
        polybius_square += chr(i)

    return polybius_square


# -------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (none)
# Return:       plaintext (string)
# Description:  Decryption using Polybius Square Cipher
#               Detects invalid ciphertext --> print error msg and return ''
#               Case 1: #of chars (other than \n) is not even
#               Case 2: the ciphertext contains non-numerical chars (except \n')
# -------------------------------------------------------
def d_polybius(ciphertext, key):
    plaintext = ''
    # your code here
    # invalid ciphertext check
    if '\n' in ciphertext:
        temp = str(ciphertext).replace('\n', '')
        if len(temp) % 2 != 0:
            print("Invalid ciphertext! Decryption Failed!")
            return ''
        if temp.isnumeric() is False:
            print("Invalid ciphertext! Decryption Failed!")
            return ''

    else:
        if len(ciphertext) % 2 != 0 or len(ciphertext) == 0:
            print("Invalid ciphertext! Decryption Failed!")
            return ''
        if ciphertext.isnumeric() is False:
            print("Invalid ciphertext! Decryption Failed!")
            return ''

    polybius_square = get_polybius_square()

    # decrypt the ciphertext
    counter = 0
    while counter < len(ciphertext):
        if ciphertext[counter] is '\n':
            plaintext += '\n'
            counter += 1
        else:
            r = int(ciphertext[counter]) - 1
            c = int(ciphertext[counter + 1]) - 1
            plaintext += polybius_square[r * 8 + c]
            counter += 2

    return plaintext


# -----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str)
# Return:       plaintext (str)
# Description:  Decryption using Hill Cipher, 2x2 (mod 26)
#               key is a string consisting of 4 characters
#                   if key is too short, make it a running key
#                   if key is too long, use first 4 characters
#               Decrypts only alphabet
#               Case of characters can be ignored --> plain is lower case
#               Remove padding of q's
# Errors:       if key is not inveritble or if ciphertext is empty
#                   print error msg and return empty string
# -----------------------------------------------------------
def d_hill(ciphertext, key):
    # your code here
    if len(ciphertext) == 0:
        print('Error(d_hill): invalid ciphertext')
        return ''

    new_key = ''
    if len(key) > 4:
        new_key += key[:4]
    elif len(key) == 4:
        new_key += key
    else:
        new_key += key
        counter = 0
        while len(new_key) < 4:
            new_key += key[counter]
            counter += 1

    baseString = utilities.get_lower()

    key_matrix = matrix.new_matrix(2, 2, 0)
    count = 0
    for i in range(2):
        for j in range(2):
            key_matrix[i][j] = baseString.index(new_key[count].lower())
            count += 1

    if mod.gcd(matrix.det(key_matrix), 26) != 1:
        print('Error(d_hill): key is not invertible')
        return ''

    inverse_key_matrix = matrix.inverse(key_matrix, 26)

    plaintext = ''
    non_alpha = utilities.get_nonalpha(ciphertext)
    blocks = utilities.text_to_blocks(utilities.remove_nonalpha(ciphertext), 2)

    for block in blocks:
        block_m = matrix.new_matrix(2, 1, 0)
        block_m[0][0] = baseString.index(block[0].lower())
        block_m[1][0] = baseString.index(block[1].lower())

        result_m = matrix.matrix_mod(matrix.mul(inverse_key_matrix, block_m), 26)

        plaintext += baseString[result_m[0][0]].lower()
        plaintext += baseString[result_m[1][0]].lower()

    plaintext = utilities.insert_nonalpha(plaintext, non_alpha)
    while plaintext[-1] == 'q':
        plaintext = plaintext[:-1]

    return plaintext


def d_Atbash(ciphertext):
    atbash = ''
    lowerChars = utilities.get_lower()
    upperChars = lowerChars.upper()
    for c in ciphertext:
        if c.isalpha():
            atbash += upperChars[ord('Z') - ord(c)] if c.isupper() else lowerChars[ord('z') - ord(c)]
        else:
            atbash += c
    return atbash


# -------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key: (shifts,direction) (int,str)
# Return:       ciphertext (string)
# Description:  Encryption using Shfit Cipher (Monoalphabetic Substitituion)
#               The alphabet is shfited as many as "shifts" using given direction
#               Non alpha characters --> no substitution
#               Valid direction = 'l' or 'r'
#               Algorithm preserves case of the characters
# ---------------------------------------------------------------------------------------
def e_shift(plaintext, key):
    alphabet = utilities.get_lower()

    shifts, direction = key
    if shifts < 0:
        shifts *= -1
        direction = 'l' if key[1] == 'r' else 'r'
    shifts = key[0] % 26
    shifts = shifts if key[1] == 'l' else 26 - shifts

    ciphertext = ''
    for char in plaintext:
        if char.lower() in alphabet:
            plainIndx = alphabet.index(char.lower())
            cipherIndx = (plainIndx + shifts) % 26
            cipherChar = alphabet[cipherIndx]
            ciphertext += cipherChar.upper() if char.isupper() else cipherChar
        else:
            ciphertext += char
    return ciphertext


# -------------------------------------------------------------------------------------
# Parameters:   ciphertext(string)
#               key: (shifts,direction) (int,str)
# Return:       ciphertext (string)
# Description:  Decryption using Shfit Cipher (Monoalphabetic Substitituion)
#               The alphabet is shfited as many as "shifts" using given direction
#               Non alpha characters --> no substitution
#               Valid direction = 'l' or 'r'
#               Algorithm preserves case of the characters
#               Trick: Encrypt using same #shifts but the other direction
# ---------------------------------------------------------------------------------------
def d_shift(ciphertext, key):
    direction = 'l' if key[1] == 'r' else 'r'
    return e_shift(ciphertext, (key[0], direction))


# -------------------------------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key,plaintext
# Description:  Cryptanalysis of shift cipher
#               Uses Chi-Square
#               Returns key and plaintext if successful
#               If cryptanalysis fails: returns '',''
# ---------------------------------------------------------------------------------------
def cryptanalysis_shift(ciphertext):
    chiList = [round(utilities.get_chiSquared(d_shift(ciphertext, (i, 'l'))), 4) for i in range(26)]
    key = chiList.index(min(chiList))
    key = (key, 'l')
    plaintext = d_shift(ciphertext, key)
    return key, plaintext


# -----------------------------------------------------------
# Parameters:   key (string)
# Return:       keyOrder (list)
# Description:  checks if given key is a valid columnar transposition key
#               Returns key order, e.g. [face] --> [1,2,3,0]
#               Removes repetitions and non-alpha characters from key
#               If empty string or not a string -->
#                   print an error msg and return [0] (which is a)
#               Upper 'A' and lower 'a' are the same order
# -----------------------------------------------------------
def get_keyOrder_columnarTrans(key):
    # your code here
    # not string
    if not isinstance(key, str):
        print('Error: Invalid Columnar Transposition Key', end=' ')
        return [0]

    # invalid key: all non-alpha
    remove_nonalpha = ''
    for char in key:
        if char.isalpha():
            remove_nonalpha += char
    if len(remove_nonalpha) == 0:
        print('Error: Invalid Columnar Transposition Key', end=' ')
        return [0]

    # valid key
    remove_repetition = ''
    for c in remove_nonalpha.lower():
        if c not in remove_repetition:
            remove_repetition += c

    # get the ranks for every character
    tempOrder = []
    for k1 in remove_repetition:
        temp = 0
        for k2 in remove_repetition:
            if ord(k1.lower()) > ord(k2.lower()):
                temp += 1
        tempOrder.append(temp)
    # get the index of the different ranks
    keyOrder = []
    for i in range(len(remove_repetition)):
        keyOrder.append(tempOrder.index(i))

    return keyOrder


# -----------------------------------------------------------
# Parameters:   ciphertext (str)
#               kye (str)
# Return:       plaintext (list)
# Description:  Decryption using Columnar Transposition Cipher
# -----------------------------------------------------------
def d_columnarTrans(ciphertext, key):
    # your code here
    key_order = get_keyOrder_columnarTrans(key)

    c = len(key_order)
    r = int(math.ceil(len(ciphertext) / c))

    matrix = utilities.new_matrix(r, c, '')

    blocks = utilities.text_to_blocks(ciphertext, r)

    # fill the matrix according to the key_order
    counter = 0
    for i in key_order:
        for j in range(r):
            matrix[j][i] = blocks[counter][j]
        counter += 1

    # read the matrix and ignore the 'q'
    plaintext = ''
    for i in range(r):
        for j in range(c):
            if matrix[i][j] != 'q':
                plaintext += matrix[i][j]

    return plaintext


def d_type1(ciphertext):
    first = d_polybius(ciphertext, '')
    plaintext = d_columnarTrans(first, 'ba')
    return plaintext, ('ba', '')


def d_type2(ciphertext):
    first = d_columnarTrans(ciphertext, 'ba')
    key, plaintext = cryptanalysis_shift(first)
    return plaintext, (key, 'ba')


def d_type3(ciphertext):
    alpha = utilities.get_lower()
    dictList = utilities.load_dictionary('engmix.txt')

    for a in range(0, 5):
        for b in range(0, 5):
            for c in range(0, 5):
                for d in range(0, 5):
                    key_matrix = matrix.new_matrix(2, 2, 0)
                    key_matrix[0][0] = a
                    key_matrix[0][1] = b
                    key_matrix[1][0] = c
                    key_matrix[1][1] = d
                    if mod.has_mul_inv(a * d - b * c, 26):
                        key = ''
                        for i in range(2):
                            for j in range(2):
                                key += alpha[key_matrix[i][j]]
                        first = d_hill(ciphertext, key)

                        k, plain = cryptanalysis_shift(first)

                        if utilities.is_plaintext(plain, dictList, 0.70):
                            return plain, (k, key)
