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
import q4


# ---------------------------------
#           Honor Pledge         #
# ---------------------------------

def honor_pledge():
    print('I certify that I have completed this final exam independently, without seeking any external help online'
          'or offline.'
          'The way I have solved this final exam reflects my moral values and ethical standards.'
          'I understand that plagiarism results in failing the course and potential suspention from the program.')
    return


# ---------------------------------
#       Q1: mathCipher          #
# ---------------------------------

def isValidKey_mathCipher(key):
    # your code here
    if not isinstance(key, tuple):
        return False
    if not isinstance(key[0], str) or not isinstance(key[1], list):
        return False
    if len(key[1]) != 3:
        return False
    for i in key[1]:
        if not isinstance(i, int):
            return False
    if len(key[0]) < 2:
        return False

    baseString = key[0]
    m = len(baseString)
    a = key[1][0]
    b = key[1][1]

    if not mod.has_mul_inv(a, m) or not mod.has_mul_inv(b, m):
        return False

    return True


def e_mathCipher(plaintext, key):
    # your code here
    if not isinstance(plaintext, str) or len(plaintext) == 0:
        print('Error(e_mathCipher): invalid plaintext', end='')
        return ''
    if not isValidKey_mathCipher(key):
        print('Error(e_mathCipher): Invalid key', end='')
        return ''

    baseString = key[0]
    m = len(baseString)
    a = key[1][0]
    b = key[1][1]
    c = key[1][2]

    ciphertext = ''
    for p in plaintext:
        if p.lower() in baseString:
            x = baseString.index(p.lower())
            y = b * (a * x + b) - c
            y = mod.residue(y, m)
            cipherChar = baseString[y]
            ciphertext += cipherChar.upper() if p.isupper() else cipherChar
        else:
            ciphertext += p

    return ciphertext


def d_mathCipher(ciphertext, key):
    # your code here
    if not isinstance(ciphertext, str) or len(ciphertext) == 0:
        print('Error(d_mathCipher): invalid ciphertext', end='')
        return ''
    if not isValidKey_mathCipher(key):
        print('Error(d_mathCipher): Invalid key', end='')
        return ''

    baseString = key[0]
    m = len(baseString)
    a = key[1][0]
    a_inv = mod.mul_inv(a, m)
    b = key[1][1]
    b_inv = mod.mul_inv(b, m)
    c_key = key[1][2]

    plaintext = ''
    for c in ciphertext:
        if c.lower() in baseString:
            y = baseString.index(c.lower())
            x = a_inv * ((y + c_key) * b_inv - b)
            x = mod.residue(x, m)
            plainChar = baseString[x]
            plaintext += plainChar.upper() if c.isupper() else plainChar
        else:
            plaintext += c

    return plaintext


def analyze_mathCipher(baseString):
    # your code here
    total = 0
    illegal = 0
    noCipher = 0
    decimation = 0
    valid = 0

    # total
    m = len(baseString)
    total = m ** 3

    # illegal
    legal = 0
    m_i_table = mod.mul_inv_table(m)
    for mi in m_i_table[1]:
        if mi != 'NA':
            legal += 1
    legal *= legal
    legal *= m
    illegal = total - legal

    # noCipher
    for mi1 in m_i_table[0]:
        if m_i_table[1][mi1] != 'NA':
            for mi2 in m_i_table[0]:
                if m_i_table[1][mi2] != 'NA':
                    for c in range(m):
                        if mod.residue(mi2 ** 2 - c, m) == 0:
                            if mod.residue(mi1 * mi2, m) == 1:
                                noCipher += 1
                            else:
                                decimation += 1
    valid = legal - decimation - noCipher

    return [total, illegal, noCipher, decimation, valid]


def stats_mathCipher():
    # your code here
    all_a = 0.0000
    all_b = 1.1000
    all_w = 0.0000

    p = 0
    p_a = 0.0000
    p_b = 1.1000
    p_w = 0.0000

    np_a = 0.0000
    np_b = 1.1000
    np_w = 0.0000

    for i in range(2, 101):
        s = ' ' * i
        ana_nums = analyze_mathCipher(s)

        total = ana_nums[0]
        valid = ana_nums[4]
        percentage = float(valid / total)

        all_a += percentage

        if percentage < all_b:
            all_b = percentage
        if percentage > all_w:
            all_w = percentage

        if mod.is_prime(i):
            p += 1
            p_a += percentage

            if percentage < p_b:
                p_b = percentage
            if percentage > p_w:
                p_w = percentage
        else:
            np_a += percentage

            if percentage < np_b:
                np_b = percentage
            if percentage > np_w:
                np_w = percentage

    print('For all numbers:')
    print('\tAverage = {0:.2f}%'.format(all_a * 100 / 99))  # <----- edit these
    print('\tBest = {0:.2f}%'.format(all_b * 100))
    print('\tWorst = {0:.2f}%'.format(all_w * 100))
    print('For Primes:')
    print('\tAverage = {0:.2f}%'.format(p_a * 100 / p))
    print('\tBest = {0:.2f}%'.format(p_b * 100))
    print('\tWorst = {0:.2f}%'.format(p_w * 100))
    print('For non Primes:')
    print('\tAverage = {0:.2f}%'.format(np_a * 100 / (99 - p)))
    print('\tBest = {0:.2f}%'.format(np_b * 100))
    print('\tWorst = {0:.2f}%'.format(np_w * 100))
    return


def cryptanalysis_mathCipher(ciphertext):
    # your code here
    baseString = utilities.get_baseString()
    length = len(baseString)
    dictList = utilities.load_dictionary('engmix.txt')

    sub_baseString = []
    for j in range(25, length):
        sub_baseString.append(baseString[:j + 1])

    attempts = 0
    for n_s in sub_baseString:
        m = len(n_s)
        m_i_table = mod.mul_inv_table(m)
        for mi1 in m_i_table[0]:
            if m_i_table[1][mi1] != 'NA':
                for mi2 in m_i_table[0]:
                    if m_i_table[1][mi2] != 'NA':
                        for c in range(m):
                            if mod.residue(mi2 ** 2 - c, m) != 0:
                                k = [mi1, mi2, c]
                                key = (n_s, k)
                                plaintext = d_mathCipher(ciphertext, key)
                                attempts += 1

                                if len(utilities.remove_nonalpha(plaintext)) < len(plaintext) / 2:
                                    continue

                                if utilities.is_plaintext(plaintext, dictList, 0.90):
                                    print('key found after ' + str(attempts) + ' attempts')
                                    return plaintext, key

    return '', ''


# ---------------------------------
# Q2: Myszkowski Cryptanalysis   #
# ---------------------------------

def e_myszkowski(plaintext, key):
    # your code here  
    key_order = get_keyOrder_myszkowski(key)
    ciphertext = ''

    c = len(key_order)
    r = int(math.ceil(len(plaintext) / c))

    matrix = utilities.new_matrix(r, c, '')

    counter = 0
    for i in range(r):
        for j in range(c):
            matrix[i][j] = plaintext[counter] if counter < len(plaintext) else 'q'
            counter += 1

    # read the matrix: unique --- vertically & repeated --- horizontally
    for i in range(c):
        for j in range(r):
            Index = 0
            while i in key_order[Index:c]:
                Index = key_order.index(i, Index, c)
                ciphertext += matrix[j][Index]
                Index += 1

    return ciphertext


def d_myszkowski(ciphertext, key):
    # your code here
    key_order = get_keyOrder_myszkowski(key)

    c = len(key_order)
    r = int(math.ceil(len(ciphertext) / c))

    matrix = utilities.new_matrix(r, c, '')

    blocks = utilities.text_to_blocks(ciphertext, r)

    # combine all the blocks of the same key character to one block
    for i in range(c):
        Index = 0
        while i in key_order[Index:c]:
            if Index != 0:
                Index = key_order.index(i, Index, c)
                blocks[key_order[Index]] += blocks[key_order[Index] + 1]
                blocks.pop(key_order[Index] + 1)

            Index = key_order.index(i, Index, c)
            Index += 1

    # fill the matrix
    for i in range(c):
        counter = 0
        for j in range(r):
            Index = 0
            while i in key_order[Index:c]:
                Index = key_order.index(i, Index, c)
                matrix[j][Index] = blocks[i][counter]
                Index += 1
                counter += 1

    # read the matrix and ignore the 'q'
    plaintext = ''
    for i in range(r):
        for j in range(c):
            if matrix[i][j] != 'q':
                plaintext += matrix[i][j]

    return plaintext


def get_keyOrder_myszkowski(key):
    # your code here
    # invalid key type 1: not string
    if not isinstance(key, str):
        print('Error: Invalid Myszkowski Key', end=' ')
        return [1, 1, 0]
    # invalid key type 2: empty string
    if len(key) == 0:
        print('Error: Invalid Myszkowski Key', end=' ')
        return [1, 1, 0]
    # invalid key type 3 & 4: all non-alpha or (no repetition or no unique char)
    remove_nonalpha = ''
    for char in key:
        if char.isalpha():
            remove_nonalpha += char
    if len(remove_nonalpha) == 0:
        print('Error: Invalid Myszkowski Key', end=' ')
        return [1, 1, 0]

    remove_repetition = ''
    for c in remove_nonalpha.lower():
        if c not in remove_repetition:
            remove_repetition += c
    if len(remove_repetition) == len(key) or len(remove_repetition) == len(key) / 2:
        print('Error: Invalid Myszkowski Key', end=' ')
        return [1, 1, 0]

    # valid key
    # get the ranks of every character
    keyOrder = []
    for k1 in remove_nonalpha:
        temp = 0
        for k2 in remove_nonalpha:
            if ord(k1.lower()) > ord(k2.lower()):
                temp += 1
        keyOrder.append(temp)

    # rearrange the rank
    for i in range(len(remove_repetition)):
        if i not in keyOrder:
            for j in range(i, len(remove_nonalpha)):
                if j in keyOrder:
                    for k in keyOrder:
                        if k == j:
                            keyOrder[keyOrder.index(k)] = i
                    break

    return keyOrder


def q2_description1():
    print('Cryptanalysis Strategy (Brute Force 3 characters): ')
    print('Put your description here:\n'
          'There must be 2 distinct characters in the key.\n'
          'So, there are only 6 kinds of key order if the length of the key is 3:\n'
          '    001 010 100 110 101 011\n'
          'And I only use \'a \' and \'b\' for the key.\n'
          'But these 2 letters can be replaced by any other 2 different letters.')  # <------------ change this line
    print('Worst Case Scenario: 6 attempts')  # <-------- change X
    print()
    return


def q2_description2():
    print('Cryptanalysis Strategy (Dictionary Attack): ')
    print('Put your description here:\n'
          'I only tried the words (given length) with at least one repeated letter\n'
          'but not all repeated letters.\n'
          'The longest word\'s length in the dictionary file is 21.\n'
          'I tried the given length ranged [3, 21] to get the worst case.\n'
          'The source code showing how I get the worst case has been commended\n'
          'in the same function q2_description2(). You can find it there.')  # <------------ change this line
    print('Worst Case Scenario: length = 9 with 10809 attempts')  # <-------- change X
    print()
    '''
    dictList = utilities.load_dictionary('engmix.txt')

    nums = []
    for length in range(3, 22):
        attempts = 0
        for l in dictList:
            for word in l:
                if len(word) == length:
                    remove_repetition = ''
                    for c in word.lower():
                        if c not in remove_repetition:
                            remove_repetition += c

                    if len(remove_repetition) != length and len(remove_repetition) != 1:
                        attempts += 1

        nums.append(attempts)

    most = nums.index(max(nums)) + 3
    print(most)
    '''
    return


def q2_description3():
    print('Cryptanalysis Strategy (5-Triple): ')
    print('Describe Brute-Force Space here:\n'
          'There can only be 3 kinds of characters in the key.\n'
          'The number of different key orders is 10 * 3 * 2 = 60 with: \n'
          '    C(5, 3) = 10 kinds of repeated positions\n'
          '    2 kinds of unrepeated letters\n'
          '    3 kinds of values --- 0, 1, 2')  # <------------ change this line
    print('Describe Dictionary space here:\n'
          'The total number of words length 5 with 3 repeated letters is 161.\n'
          'The source code showing how I get the number has been commended\n'
          'in the same function q2_description3(). You can find it there.')  # <------------ change this line
    print('60 is better than 161 (Brute-Force Space is better.)')  # <------------ change this line
    '''
    dictList = utilities.load_dictionary('engmix.txt')

    nums = []
    length = 5
    attempts = 0
    for l in dictList:
        for word in l:
            if len(word) == length:
                remove_repetition = ''
                type = 0
                for c in word.lower():
                    if c not in remove_repetition:
                        remove_repetition += c
                        type += 1

                if len(word) - len(remove_repetition) == 2 and type == 3:
                    attempts += 1
    print(attempts)
    '''
    print()
    return


def cryptanalysis1_myszkowski(ciphertext):
    # your code here
    possible = ['aab', 'aba', 'baa', 'bba', 'bab', 'abb']
    dictList = utilities.load_dictionary('engmix.txt')

    attempts = 0
    for pos in possible:
        plaintext = d_myszkowski(ciphertext, pos)
        attempts += 1

        if utilities.is_plaintext(plaintext, dictList, 0.90):
            print('key found after ' + str(attempts) + ' attempts')
            return plaintext, pos

    return '', ''


def cryptanalysis2_myszkowski(ciphertext, length):
    # your code here
    dictList = utilities.load_dictionary('engmix.txt')

    attempts = 0
    for l in dictList:
        for word in l:
            if len(word) == length:
                remove_repetition = ''
                for c in word.lower():
                    if c not in remove_repetition:
                        remove_repetition += c

                if len(remove_repetition) != length and len(remove_repetition) != 1:
                    plaintext = d_myszkowski(ciphertext, word)
                    attempts += 1

                    if utilities.is_plaintext(plaintext, dictList, 0.90):
                        print('key found after ' + str(attempts) + ' attempts')
                        return plaintext, word

    return '', ''


def cryptanalysis3_myszkowski(ciphertext):
    # your code here
    init_list = [[0, 0, 0, 1, 2], [1, 1, 1, 0, 2], [2, 2, 2, 0, 1]]
    lower = utilities.get_lower()
    dictList = utilities.load_dictionary('engmix.txt')

    attempts = 0
    for init in init_list:
        combinations = SDES.combinations(init)
        for com in combinations:
            key = ''
            for num in com:
                key += lower[num]

            plaintext = d_myszkowski(ciphertext, key)
            attempts += 1

            if utilities.is_plaintext(plaintext, dictList, 0.80):
                print('key found after ' + str(attempts) + ' attempts')
                return plaintext, key

    return '', ''


# ---------------------------------
#           Q3: SDES Modes       #
# ---------------------------------
# generic functions - specific functions in SDES.py
def e_SDES(plaintext, key, mode):
    # your code here
    modes = ['ECB', 'CBC', 'OFB']
    if mode not in modes:
        print('Error(e_SDES): undefined mode', end='')
        return ''
    if not isinstance(plaintext, str) or len(plaintext) == 0:
        print('Error(e_SDES): Invalid input', end='')
        return ''

    if len(key) == 0:
        if SDES.get_SDES_value('p') == '' or SDES.get_SDES_value('q') == '' or SDES.get_SDES_value('key_size') == '':
            print('Error(e_SDES): Invalid key', end='')
            return ''
        key = SDES.generate_key_SDES()
    if not utilities.is_binary(key):
        print('Error(e_SDES): Invalid key', end='')
        return ''
    if SDES.get_SDES_value('key_size') == '' or len(key) != int(SDES.get_SDES_value('key_size')):
        print('Error(e_SDES): Invalid key', end='')
        return ''

    if mode == modes[0]:
        return SDES.e_SDES_ECB(plaintext, key)
    elif mode == modes[1]:
        return SDES.e_SDES_CBC(plaintext, key)
    else:
        return SDES.e_SDES_OFB(plaintext, key)


def d_SDES(ciphertext, key, mode):
    # your code here
    modes = ['ECB', 'CBC', 'OFB']
    if mode not in modes:
        print('Error(d_SDES): undefined mode', end='')
        return ''
    if not isinstance(ciphertext, str) or len(ciphertext) == 0:
        print('Error(d_SDES): Invalid input', end='')
        return ''

    if len(key) == 0:
        if SDES.get_SDES_value('p') == '' or SDES.get_SDES_value('q') == '' or SDES.get_SDES_value('key_size') == '':
            print('Error(d_SDES): Invalid key', end='')
            return ''
        key = SDES.generate_key_SDES()
    if not utilities.is_binary(key):
        print('Error(d_SDES): Invalid key', end='')
        return ''
    if len(key) != int(SDES.get_SDES_value('key_size')):
        print('Error(d_SDES): Invalid key', end='')
        return ''

    if mode == modes[0]:
        return SDES.d_SDES_ECB(ciphertext, key)
    elif mode == modes[1]:
        return SDES.d_SDES_CBC(ciphertext, key)
    else:
        return SDES.d_SDES_OFB(ciphertext, key)


# ---------------------------------
#           Q4: Double X       #
# ---------------------------------
# Specific functions are in q4.py
def q4A(ciphertext):
    # your code here
    print('Provide your description here:\n'
          'The ciphertext is all numbers --> the second step would be Polybius.\n'
          'After decryption of Polybius, I start to decrypt the new cipher with easier ways.\n'
          'First Atbash --> is_plaintext() is False\n'
          'Second Shift Cryptanalysis --> False.\n'
          'Third Columnar Transposition(only with key \'ba\') --> True\n'
          'The result is: Columnar Transposition + Polybius')  # <----- edit this
    plaintext, (key2, key1) = q4.d_type1(ciphertext)
    utilities.text_to_file(plaintext, 'q4A_plaintext.txt')
    return plaintext, (key1, key2)


def q4B(ciphertext):
    # your code here
    print('Provide your description here:\n'
          'There are so many \'q\'s in the ciphertext. The only way of encryption with\n'
          'padding q is Columnar Transposition.\n'
          'The new cipher can not be Polybius (not numbers).\n'
          'It can not be Hill cipher since Columnar Transposition does not change cases of letters.\n'
          'So, I still start from the easier ways.\n'
          'First Atbash --> is_plaintext() is False\n'
          'Second Shift Cryptanalysis --> True.\n'
          'The result is: Shift + Columnar Transposition')  # <----- edit this
    plaintext, (key2, key1) = q4.d_type2(ciphertext)
    utilities.text_to_file(plaintext, 'q4B_plaintext.txt')
    return plaintext, (key1, key2)


def q4C(ciphertext):
    # your code here
    print('Provide your description here:\n'
          'All the characters of the ciphertext are upper case --> It must be Hill Cipher.\n'
          'I have writen a simple cryptanalysis function.\n'
          'I constructed  all the 2by2 matrix which are invertible. And after I got each new cipher,\n'
          'I tried all the possible 3 ways:\n'
          '        Atbash & Columnar Transposition & Shift\n'
          '        It can\'t be Polybius since there is no numbers.'
          'The cryptanalysis has failed for the first 2 ways but returned the right text for Shift Cipher.\n'
          'The result is: Shift + Hill')  # <----- edit this
    plaintext, (key2, key1) = q4.d_type3(ciphertext)
    utilities.text_to_file(plaintext, 'q4C_plaintext.txt')
    return plaintext, (key1, key2)


# ---------------------------------
# Q5: Public Key Cryptography    #
# ---------------------------------
def get_RSAKey():
    # your code here
    name = 'Jiayao_Pang'
    p = 21217033
    q = 23453233
    n = (p - 1) * (q - 1)
    m = 497608018517689
    e = 32452885
    d = mod.mul_inv(e, n)
    return [name, p, q, m, n, e, d]


def LRM(b, e, m):
    # your code here
    binary = utilities.dec_to_bin(e, 100)
    i = binary.find('1')
    binary = binary[i:]

    x = mod.residue(b, m)
    first = True
    for bit in binary:
        if first:
            first = False
        else:
            x = mod.residue(x ** 2, m)
            if bit == '1':
                x = mod.residue(x * b, m)

    x = mod.residue(x, m)
    return x


def encode_mod96(text):
    # your code here
    baseString = utilities.get_RSA_baseString()

    i_list = []
    for p in text:
        i = baseString.index(p)
        i_list.append(i)

    num = 0
    length = len(i_list) - 1
    counter = 0
    for i in i_list:
        num += (96 ** (length - counter)) * i
        counter += 1

    return num


def decode_mod96(num, block_size):
    # your code here
    base96 = []
    q = 1
    r = 0
    while q != 0:
        q = num // 96
        r = num % 96
        num = q
        base96.append(r)

    base96.reverse()

    baseString = utilities.get_RSA_baseString()
    text = ''
    for i in base96:
        text += baseString[i]

    while len(text) < block_size:
        text = 'a' + text

    return text


def e_RSA(plaintext, key):
    # your code here
    blocks = utilities.text_to_blocks(plaintext, 6)
    while len(blocks[-1]) != 6:
        blocks[-1] += 'q'

    ciphertext = ''
    for block in blocks:
        num = encode_mod96(block)
        y = LRM(num, key[1], key[0])
        ciphertext += decode_mod96(y, 8)

    return ciphertext


def d_RSA(ciphertext, key):
    # your code here
    blocks = utilities.text_to_blocks(ciphertext, 8)

    plaintext = ''
    for block in blocks:
        c = encode_mod96(block)
        p = LRM(c, key[1], key[0])
        plaintext += decode_mod96(p, 6)

    while plaintext[-1] == 'q':
        plaintext = plaintext[:-1]

    return plaintext


def verify_RSA(message):
    # your code here
    file = open('public_keys.txt', 'r')
    content = file.read()
    info = content.split('\n')

    public_keys = []
    for i in info:
        temp = i.split(' ')
        public_keys.append(temp)

    dictList = utilities.load_dictionary('engmix.txt')

    for key in public_keys:
        plaintext = d_RSA(message, (int(key[1]), int(key[2])))

        if utilities.is_plaintext(plaintext, dictList, 0.90):
            return key[0], plaintext

    return 'Unknown', ''

# ----------------------------
#           Good Luck
# ----------------------------
