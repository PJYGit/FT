# --------------------------
# CP460 (Fall 2019)
# Final Exam
# Jiayao Pang
# 194174300
# --------------------------

# Put your SDES.py implementation here
import math
import string
import mod
import utilities

configFile = 'SDES_config.txt'
sbox1File = 'sbox1.txt'
sbox2File = 'sbox2.txt'
primeFile = 'primes.txt'


# -----------------------
# Q1: Coding Scheme
# -----------------------
# -----------------------------------------------------------
# Parameters:   c (str): a character
#               codeType (str)
# Return:       b (str): corresponding binary number
# Description:  Generic function for encoding
#               Current implementation supports only ASCII and B6 encoding
# Error:        If c is not a single character:
#                   print('Error(encode): invalid input'), return ''
#               If unsupported encoding type:
#                   print('Error(encode): Unsupported Coding Type'), return ''
# -----------------------------------------------------------
def encode(c, codeType):
    # your code here
    if not isinstance(c, str):
        print('Error(encode): invalid input', end='')
        return ''
    if len(c) != 1:
        print('Error(encode): invalid input', end='')
        return ''
    if not isinstance(codeType, str):
        print('Error(encode): Unsupported Coding Type', end='')
        return ''
    if str(codeType) != 'B6' and str(codeType) != 'ASCII':
        print('Error(encode): Unsupported Coding Type', end='')
        return ''

    if codeType == 'B6':
        b = encode_B6(c)
    else:
        b = utilities.dec_to_bin(ord(c), 8)

    return b


# -----------------------------------------------------------
# Parameters:   b (str): a binary number
#               codeType (str)
# Return:       c (str): corresponding character
# Description:  Generic function for decoding
#               Current implementation supports only ASCII and B6 encoding
# Error:        If b is not a binary number:
#                   print('Error(decode): invalid input',end =''), return ''
#               If unsupported encoding type:
#                   print('Error(decode): Unsupported Coding Type',end =''), return ''
# -----------------------------------------------------------
def decode(b, codeType):
    # your code here
    if not utilities.is_binary(b):
        print('Error(decode): invalid input', end='')
        return ''
    if not isinstance(codeType, str):
        print('Error(decode): Unsupported Coding Type', end='')
        return ''
    if str(codeType) != 'B6' and str(codeType) != 'ASCII':
        print('Error(decode): Unsupported Coding Type', end='')
        return ''

    if codeType == 'ASCII':
        c = chr(utilities.bin_to_dec(b))
    else:
        c = decode_B6(b)

    return c


# -----------------------------------------------------------
# Parameters:   c (str): a character
# Return:       b (str): 6-digit binary code
# Description:  Encodes any given symbol in the B6 Encoding scheme
#               If given symbol is one of the 64 symbols, the function returns
#               the binary representation, which is the equivalent binary number
#               of the decimal value representing the position of the symbol in the B6Code
#               If the given symbol is not part of the B6Code --> return empty string (no error msg)
# Error:        If given input is not a single character -->
#                   print('Error(encode_B6): invalid input',end =''), return ''
# -----------------------------------------------------------
def encode_B6(c):
    # your code here
    if not isinstance(c, str):
        print('Error(encode_B6): invalid input', end='')
        return ''
    if len(c) != 1:
        print('Error(encode_B6): invalid input', end='')
        return ''

    b6_code = utilities.get_B6Code()

    if c not in b6_code:
        return ''

    i = b6_code.index(c)
    b = utilities.dec_to_bin(i, 6)

    return b


# -----------------------------------------------------------
# Parameters:   b (str): binary number
# Return:       c (str): a character
# Description:  Decodes any given binary code in the B6 Coding scheme
#               Converts the binary number into integer, then get the
#               B6 code at that position
# Error:        If given input is not a valid 6-bit binary number -->
#                   print('Error(decode_B6): invalid input',end =''), return ''
# -----------------------------------------------------------
def decode_B6(b):
    # your code here
    if not utilities.is_binary(b):
        print('Error(decode_B6): invalid input', end='')
        return ''
    if len(b) != 6:
        print('Error(decode_B6): invalid input', end='')
        return ''

    b6_code = utilities.get_B6Code()
    c = b6_code[utilities.bin_to_dec(b)]

    return c


# -----------------------
# Q2: SDES Configuration
# -----------------------
# -----------------------------------------------------------
# Parameters:   None
# Return:       paramList (list)
# Description:  Returns a list of parameter names which are used in
#               Configuration of SDES
# Error:        None
# -----------------------------------------------------------
def get_SDES_parameters():
    return ['encoding_type', 'block_size', 'key_size', 'rounds', 'p', 'q']


# -----------------------------------------------------------
# Parameters:   None
# Return:       configList (2D List)
# Description:  Returns the current configuration of SDES
#               configuration list is formatted as the following:
#               [[parameter1,value],[parameter2,value2],...]
#               The configurations are read from the configuration file
#               If configuration file is empty --> return []
# Error:        None
# -----------------------------------------------------------
def get_SDES_config():
    # your code here
    config = open(configFile, 'r')
    content = config.read()

    if len(content) == 0:
        return []

    values = content.split(' ')
    parameters = get_SDES_parameters()

    configList = []
    for v in values:
        if v in parameters:
            temp = [v, values[values.index(v) + 1]]
            configList.append(temp)

    return configList


# -----------------------------------------------------------
# Parameters:   parameter (str)
# Return:       value (str)
# Description:  Returns the value of the parameter based on the current
# Error:        If the parameter is undefined in get_SDES_parameters() -->
#                   print('Error(get_SDES_value): invalid parameter',end =''), return ''
# -----------------------------------------------------------
def get_SDES_value(parameter):
    # your code here
    p = get_SDES_parameters()

    if str(parameter) not in p:
        print('Error(get_SDES_value): invalid parameter', end='')
        return ''

    config = get_SDES_config()
    if len(config) == 0:
        return ''
    found = False
    for c in config:
        if str(parameter) == c[0]:
            value = c[1]
            found = True
            break
    if not found:
        return ''

    return value


# -----------------------------------------------------------
# Parameters:   parameter (str)
#               value (str)
# Return:       True/False
# Description:  Sets an SDES parameter to the given value and stores
#               the output in the configuration file
#               if the configuration file contains previous value for the parameter
#               the function overrides it with the new value
#               otherwise, the new value is appended to the configuration file
#               Function returns True if set value is successful and False otherwise
# Error:        If the parameter is undefined in get_SDES_parameters() -->
#                   print('Error(cofig_SDES): invalid parameter',end =''), return False
#               If given value is not a string or is an empty string:
#                   print('Error(config_SDES): invalid value',end =''), return 'False
# -----------------------------------------------------------
def config_SDES(parameter, value):
    # your code here
    p = get_SDES_parameters()

    if str(parameter) not in p:
        print('Error(cofig_SDES): invalid parameter', end='')
        return False
    if not isinstance(value, str):
        print('Error(config_SDES): invalid value', end='')
        return False
    if len(value) == 0:
        print('Error(config_SDES): invalid value', end='')
        return False

    config = get_SDES_config()

    if len(config) == 0:
        temp = [parameter, value]
        config.append(temp)

        cf = open(configFile, 'w')
        for c in config:
            cf.write(c[0] + ' ' + c[1] + ' ')
        cf.close()
        return True

    found = False
    for c in config:
        if parameter == c[0]:
            c[1] = value
            found = True
            break
    if not found:
        temp = [parameter, value]
        config.append(temp)

    cf = open(configFile, 'w')
    for c in config:
        cf.write(c[0] + ' ' + c[1] + ' ')
    cf.close()

    return True


# -----------------------
# Q3: Key Generation
# -----------------------
# -----------------------------------------------------------
# Parameters:   p (int)
#               q (int)
#               m (int): number of bits
# Return:       bitStream (str)
# Description:  Uses Blum Blum Shub Random Generation Algorithm to generates
#               a random stream of bits of size m
#               The seed is the nth prime number, where n = p*q
#               If the nth prime number is not relatively prime with n,
#               the next prime number is selected until a valid one is found
#               The prime numbers are read from the file primeFile (starting n=1)
# Error:        If number of bits is not a positive integer -->
#                   print('Error(blum): Invalid value of m',end =''), return ''
#               If p or q is not an integer that is congruent to 3 mod 4:
#                   print('Error(blum): Invalid values of p,q',end =''), return ''
# -----------------------------------------------------------
def blum(p, q, m):
    # your code here
    if not isinstance(m, int):
        print('Error(blum): Invalid value of m', end='')
        return ''
    if m <= 0:
        print('Error(blum): Invalid value of m', end='')
        return ''
    if not isinstance(p, int) or not isinstance(q, int):
        print('Error(blum): Invalid values of p,q', end='')
        return ''
    if mod.residue(p, 4) != 3 or mod.residue(q, 4) != 3:
        print('Error(blum): Invalid values of p,q', end='')
        return ''

    n = p * q

    p_file = open(primeFile, 'r')
    primes = p_file.read().split('\n')

    temp = n
    seed = int(primes[temp - 1])
    while mod.gcd(seed, n) != 1:
        temp += 1
        seed = int(primes[temp - 1])

    bitStream = ''

    x = mod.residue(seed ** 2, n)
    for i in range(m):
        x = mod.residue(x ** 2, n)
        bitStream += str(mod.residue(x, 2))

    return bitStream


# -----------------------------------------------------------
# Parameters:   None
# Return:       key (str)
# Description:  Generates an SDES key based on preconfigured values
#               The key size is fetched from the SDES configuration
#               If no key size is available, an error message is printed
#               Also, the values of p and q are fetched as per SDES configuration
#               If no values are found, the default values p = 383 and q = 503 are used
#               These values should be updated in the configuration file
#               The function calls the blum function to generate the key
# Error:        if key size is not defined -->
#                           print('Error(generate_key_SDES):Unknown Key Size',end=''), return ''
# -----------------------------------------------------------
def generate_key_SDES():
    # your code here
    if get_SDES_value('key_size') == '':
        print('Error(generate_key_SDES):Unknown Key Size', end='')
        return ''
    if get_SDES_value('p') == '':
        config_SDES('p', '383')
    if get_SDES_value('q') == '':
        config_SDES('q', '503')

    p = int(get_SDES_value('p'))
    q = int(get_SDES_value('q'))
    key_size = int(get_SDES_value('key_size'))

    key = blum(p, q, key_size)

    return key


# -----------------------------------------------------------
# Parameters:   key (str)
#               i (int)
# Return:       key (str)
# Description:  Generates a subkey for the ith round in SDES
#               The sub-key is one character shorter than original key size
#               Sub-key is generated by circular shift of key with value 1,
#               where i=1 means no shift
#               The least significant bit is dropped after the shift
# Errors:       if key is not a valid binary number or its length does not match key_size: -->
#                   print('Error(get_subKey): Invalid key',end='')
#               if i is not a positive integer:
#                   print('Error(get_subKey): invalid i',end=''), return ''
# -----------------------------------------------------------
def get_subKey(key, i):
    # your code here
    if not utilities.is_binary(key):
        print('Error(get_subKey): Invalid key', end='')
        return ''
    if len(key) != int(get_SDES_value('key_size')):
        print('Error(get_subKey): Invalid key', end='')
        return ''
    if not isinstance(i, int):
        print('Error(get_subKey): invalid i', end='')
        return ''
    if i <= 0:
        print('Error(get_subKey): invalid i', end='')
        return ''

    if i == 1:
        subKey = key[:-1]
    else:
        subKey = key[i - 1:] + key[:i - 2]

    return subKey


# -----------------------
# Q4: Fiestel Network
# -----------------------
# -----------------------------------------------------------
# Parameters:   R (str): binary number of size (block_size/2)
# Return:       output (str): expanded binary
# Description:  Expand the input binary number by adding two digits
#               The input binary number should be an even number >= 6
#               Expansion works as the following:
#               If the index of the two middle elements is i and i+1
#               From indices 0 up to i-1: same order
#               middle becomes: R(i+1)R(i)R(i+1)R(i)
#               From incides R(i+2) to the end: same order
# Error:        if R not a valid binary number or if it has an odd length
#               or is of length smaller than 6
#                   print('Error(expand): invalid input',end=''), return ''
# -----------------------------------------------------------
def expand(R):
    # your code here
    if not utilities.is_binary(R) or len(R) < 6 or len(R) % 2 != 0:
        print('Error(expand): invalid input', end='')
        return ''

    mid = int(len(R) / 2)
    t1 = R[mid - 1]
    t2 = R[mid]
    output = R[:mid - 1] + t2 + t1 + t2 + t1 + R[mid + 1:]

    return output


# -----------------------------------------------------------
# Parameters:   R (str): binary number of size (block_size//4)
# Return:       output (str): binary number
# Description:  Validates that R is of size block_size//4 + 1
#               Retrieves relevant structure of sbox1 from sbox1File
#               Most significant bit of R is row number, other bits are column number
# Error:        if undefined block_size:
#                   print('Error(sbox1): undefined block size',end=''), return ''
#               if invalid R:
#                   print('Error(sbox1): invalid input',end=''),return ''
#               if no sbox1 structure exist:
#                   print('Error(sbox1): undefined sbox1',end=''),return ''
# -----------------------------------------------------------
def sbox1(R):
    # your code here
    if get_SDES_value('block_size') == '':
        print('Error(sbox1): undefined block size', end='')
        return ''
    if not utilities.is_binary(R):
        print('Error(sbox1): invalid input', end='')
        return ''
    if len(R) != int(int(get_SDES_value('block_size')) / 4 + 1):
        print('Error(sbox1): invalid input', end='')
        return ''

    sbox1_file = open(sbox1File, 'r')
    sbox1_list = sbox1_file.read().split('\n')

    if len(R) - 1 > len(sbox1_list):
        print('Error(sbox1): undefined sbox1', end='')
        return ''

    box_2d = []
    for box in sbox1_list:
        box = box[box.find(':') + 1:]
        box_2d.append(box.split(','))

    row = int(utilities.bin_to_dec(R[0]))
    column = int(utilities.bin_to_dec(R[1:]))

    temp = 2 ** (len(R) - 1)

    try:
        output = box_2d[len(R) - 2][row * temp + column]
    except IndexError:
        print('Error(sbox1): undefined sbox1', end='')
        return ''

    return output


# -----------------------------------------------------------
# Parameters:   R (str): binary number of size (block_size//4)
# Return:       output (str): binary
# Description:  Validates that R is of size block_size//4 + 1
#               Retrieves relevant structure of sbox2 from sbox2File
#               Most significant bit of R is row number, other bits are column number
# Error:        if undefined block_size:
#                   print('Error(sbox2): undefined block size',end=''), return ''
#               if invalid R:
#                   print('Error(sbox2): invalid input',end=''),return ''
#               if no sbox1 structure exist:
#                   print('Error(sbox2): undefined sbox1',end=''),return ''
# -----------------------------------------------------------
def sbox2(R):
    # your code here
    if get_SDES_value('block_size') == '':
        print('Error(sbox2): undefined block size', end='')
        return ''
    if not utilities.is_binary(R):
        print('Error(sbox2): invalid input', end='')
        return ''
    if len(R) != int(int(get_SDES_value('block_size')) / 4 + 1):
        print('Error(sbox2): invalid input', end='')
        return ''

    sbox2_file = open(sbox2File, 'r')
    sbox2_list = sbox2_file.read().split('\n')

    if len(R) - 1 > len(sbox2_list):
        print('Error(sbox2): undefined sbox2', end='')
        return ''

    box_2d = []
    for box in sbox2_list:
        box = box[box.find(':') + 1:]
        box_2d.append(box.split(','))

    row = int(utilities.bin_to_dec(R[0]))
    column = int(utilities.bin_to_dec(R[1:]))

    temp = 2 ** (len(R) - 1)

    try:
        output = box_2d[len(R) - 2][row * temp + column]
    except IndexError:
        print('Error(sbox2): undefined sbox2', end='')
        return ''

    return output


# -----------------------------------------------------------
# Parameters:   Ri (str): block of binary numbers
#               ki (str): binary number representing subkey
# Return:       Ri2 (str): block of binary numbers
# Description:  Performs the following five tasks:
#               1- Pass the Ri block to the expander function
#               2- Xor the output of [1] with ki
#               3- Divide the output of [2] into two equal sub-blocks
#               4- Pass the most significant bits of [3] to Sbox1
#                  and least significant bits to sbox2
#               5- Conactenate the output of [4] as [sbox1][sbox2]
# Error:        if ki is an invalid binary number:
#                   print('Error(F): invalid key',end=''), return ''
#               if invalid Ri:
#                   print('Error(F): invalid input',end=''),return ''
# -----------------------------------------------------------
def F(Ri, ki):
    # your code here
    if not utilities.is_binary(ki):
        print('Error(F): invalid key', end='')
        return ''
    if len(ki) != int(get_SDES_value('key_size')) - 1:
        print('Error(F): invalid key', end='')
        return ''
    if not utilities.is_binary(Ri):
        print('Error(F): invalid input', end='')
        return ''
    if len(Ri) != int(get_SDES_value('block_size')) / 2:
        print('Error(F): invalid input', end='')
        return ''

    expanded = expand(Ri)
    xored = utilities.xor(expanded, ki)

    b1 = sbox1(xored[:int(len(xored) / 2)])
    b2 = sbox2(xored[int(len(xored) / 2):])

    Ri2 = b1 + b2

    return Ri2


# -----------------------------------------------------------
# Parameters:   bi (str): block of binary numbers
#               ki (str): binary number representing subkey
# Return:       bi2 (str): block of binary numbers
# Description:  Applies Fiestel Cipher on a block of binary numbers
#               L(current) = R(previous)
#               R(current) = L(previous)xor F(R(previous), subkey)
# Error:        if ki is an invalid binary number or of invalid size
#                   print('Error(feistel): Invalid key',end=''), return ''
#               if invalid Ri:
#                   print('Error(feistel): Invalid block',end=''),return ''
# -----------------------------------------------------------
def feistel(bi, ki):
    # your code here
    if not utilities.is_binary(ki) or len(ki) != int(get_SDES_value('key_size')) - 1:
        print('Error(feistel): Invalid key', end='')
        return ''
    if not utilities.is_binary(bi) or len(bi) != int(get_SDES_value('block_size')):
        print('Error(feistel): Invalid block', end='')
        return ''

    after_F = F(bi[int(len(bi) / 2):], ki)
    after_xor = utilities.xor(after_F, bi[:int(len(bi) / 2)])

    bi2 = bi[int(len(bi) / 2):] + after_xor

    return bi2


# ----------------------------------
# Q5: SDES Encryption/Decryption
# ----------------------------------
# -----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (str)
# Return:       ciphertext (str)
# Description:  Encryption using Simple DES
# -----------------------------------------------------------
def e_SDES_ECB(plaintext, key):
    # your code here
    if not isinstance(plaintext, str) or len(plaintext) == 0:
        print('Error(e_SDES_ECB): Invalid input', end='')
        return ''
    if get_SDES_value('encoding_type') == '' or get_SDES_value('block_size') == '' or get_SDES_value('key_size') == '':
        print('Error(e_SDES_ECB): Invalid configuration', end='')
        return ''

    if len(key) == 0:
        if get_SDES_value('p') == '' or get_SDES_value('q') == '' or get_SDES_value('key_size') == '':
            print('Error(e_SDES_ECB): Invalid key', end='')
            return ''
        key = generate_key_SDES()
    if not utilities.is_binary(key):
        print('Error(e_SDES_ECB): Invalid key', end='')
        return ''
    if len(key) != int(get_SDES_value('key_size')):
        print('Error(e_SDES_ECB): Invalid key', end='')
        return ''

    undefined = utilities.get_undefined(plaintext, utilities.get_B6Code())
    text = utilities.remove_undefined(plaintext, utilities.get_B6Code())
    size = int(int(get_SDES_value('block_size')) / 6)
    blocks = utilities.text_to_blocks(text, size)
    while len(blocks[-1]) != size:
        blocks[-1] += 'Q'

    ciphertext = ''
    for block in blocks:
        cipher_block = ''
        for b in block:
            cipher_block += encode_B6(b)

        for i in range(int(get_SDES_value('rounds'))):
            cipher_block = feistel(cipher_block, get_subKey(key, i + 1))

        cipher_block = cipher_block[int(len(cipher_block) / 2):] + cipher_block[:int(len(cipher_block) / 2)]

        b_blocks = utilities.text_to_blocks(cipher_block, 6)
        for b_b in b_blocks:
            ciphertext += decode_B6(b_b)

    ciphertext = utilities.insert_undefinedList(ciphertext, undefined)

    return ciphertext


# -----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str)
# Return:       plaintext (str)
# Description:  Decryption using Simple DES
# -----------------------------------------------------------
def d_SDES_ECB(ciphertext, key):
    # your code here
    if not isinstance(ciphertext, str) or len(ciphertext) == 0:
        print('Error(d_SDES_ECB): Invalid input', end='')
        return ''
    if get_SDES_value('encoding_type') == '' or get_SDES_value('block_size') == '' or get_SDES_value('key_size') == '':
        print('Error(d_SDES_ECB): Invalid configuration', end='')
        return ''

    if len(key) == 0:
        if get_SDES_value('p') == '' or get_SDES_value('q') == '' or get_SDES_value('key_size') == '':
            print('Error(d_SDES_ECB): Invalid key', end='')
            return ''
        key = generate_key_SDES()
    if not utilities.is_binary(key):
        print('Error(d_SDES_ECB): Invalid key', end='')
        return ''
    if len(key) != int(get_SDES_value('key_size')):
        print('Error(d_SDES_ECB): Invalid key', end='')
        return ''

    undefined = utilities.get_undefined(ciphertext, utilities.get_B6Code())
    text = utilities.remove_undefined(ciphertext, utilities.get_B6Code())
    size = int(int(get_SDES_value('block_size')) / 6)
    blocks = utilities.text_to_blocks(text, size)

    plaintext = ''
    for block in blocks:
        plain_block = ''
        for b in block:
            plain_block += encode_B6(b)

        rounds = int(get_SDES_value('rounds'))
        for i in range(rounds):
            plain_block = feistel(plain_block, get_subKey(key, rounds - i))

        plain_block = plain_block[int(len(plain_block) / 2):] + plain_block[:int(len(plain_block) / 2)]

        b_blocks = utilities.text_to_blocks(plain_block, 6)
        for b_b in b_blocks:
            plaintext += decode_B6(b_b)

    while plaintext[-1] == 'Q':
        plaintext = plaintext[:-1]

    plaintext = utilities.insert_undefinedList(plaintext, undefined)

    return plaintext


# -------------------------------------------------------------------
# Parameters:   init (str)
# Return:       resultList (2D list)
# Description:  Construction of the combinations with the given list
# -------------------------------------------------------------------
def combinations(init):
    if init is None:
        return None
    if len(init) == 1:
        return [init]
    res = []
    left = init[0]
    right = combinations(init[1:])
    for i in right:
        for j in range(len(i) + 1):
            res.append(i[:j] + [left] + i[j:])

    resultList = []
    for item in res:
        if item not in resultList:
            resultList.append(item)

    return resultList


def e_SDES_CBC(plaintext, key):
    undefined = utilities.get_undefined(plaintext, utilities.get_B6Code())
    text = utilities.remove_undefined(plaintext, utilities.get_B6Code())
    size = int(int(get_SDES_value('block_size')) / 6)
    blocks = utilities.text_to_blocks(text, size)
    while len(blocks[-1]) != size:
        blocks[-1] += 'Q'

    IV = get_IV()

    ciphertext = ''
    for block in blocks:
        cipher_block = ''
        for b in block:
            cipher_block += encode_B6(b)

        cipher_block = utilities.xor(cipher_block, IV)

        for i in range(int(get_SDES_value('rounds'))):
            cipher_block = feistel(cipher_block, get_subKey(key, i + 1))

        cipher_block = cipher_block[int(len(cipher_block) / 2):] + cipher_block[:int(len(cipher_block) / 2)]

        b_blocks = utilities.text_to_blocks(cipher_block, 6)
        for b_b in b_blocks:
            ciphertext += decode_B6(b_b)

        IV = cipher_block

    ciphertext = utilities.insert_undefinedList(ciphertext, undefined)

    return ciphertext


def d_SDES_CBC(ciphertext, key):
    undefined = utilities.get_undefined(ciphertext, utilities.get_B6Code())
    text = utilities.remove_undefined(ciphertext, utilities.get_B6Code())
    size = int(int(get_SDES_value('block_size')) / 6)
    blocks = utilities.text_to_blocks(text, size)

    plaintext = ''
    IV = get_IV()
    temp = ''
    for block in blocks:
        plain_block = ''
        for b in block:
            plain_block += encode_B6(b)
        temp = plain_block

        rounds = int(get_SDES_value('rounds'))
        for i in range(rounds):
            plain_block = feistel(plain_block, get_subKey(key, rounds - i))

        plain_block = plain_block[int(len(plain_block) / 2):] + plain_block[:int(len(plain_block) / 2)]

        plain_block = utilities.xor(IV, plain_block)

        b_blocks = utilities.text_to_blocks(plain_block, 6)
        for b_b in b_blocks:
            plaintext += decode_B6(b_b)

        IV = temp

    while plaintext[-1] == 'Q':
        plaintext = plaintext[:-1]

    plaintext = utilities.insert_undefinedList(plaintext, undefined)

    return plaintext


def get_IV(block_size=12):
    block_size = int(get_SDES_value('block_size'))
    return blum(643, 131, block_size)


def e_SDES_OFB(plaintext, key):
    undefined = utilities.get_undefined(plaintext, utilities.get_B6Code())
    text = utilities.remove_undefined(plaintext, utilities.get_B6Code())
    size = int(int(get_SDES_value('block_size')) / 6)
    blocks = utilities.text_to_blocks(text, size)

    IV = get_IV()
    ciphertext = ''
    counter = 0
    for block in blocks:
        temp = ''
        cipher_block = IV
        for i in range(int(get_SDES_value('rounds'))):
            cipher_block = feistel(cipher_block, get_subKey(key, i + 1))

        cipher_block = cipher_block[int(len(cipher_block) / 2):] + cipher_block[:int(len(cipher_block) / 2)]

        IV = cipher_block

        for b in block:
            temp += encode_B6(b)

        if counter <= len(blocks) - 2:
            cipher_block = utilities.xor(cipher_block, temp)
        else:
            cipher_block = utilities.xor(temp, cipher_block[:len(temp)])

        b_blocks = utilities.text_to_blocks(cipher_block, 6)
        for b_b in b_blocks:
            ciphertext += decode_B6(b_b)

        counter += 1

    ciphertext = utilities.insert_undefinedList(ciphertext, undefined)

    return ciphertext


def d_SDES_OFB(ciphertext, key):
    undefined = utilities.get_undefined(ciphertext, utilities.get_B6Code())
    text = utilities.remove_undefined(ciphertext, utilities.get_B6Code())
    size = int(int(get_SDES_value('block_size')) / 6)
    blocks = utilities.text_to_blocks(text, size)

    IV = get_IV()
    plaintext = ''
    counter = 0
    for block in blocks:
        temp = ''
        plain_block = IV
        rounds = int(get_SDES_value('rounds'))
        for i in range(rounds):
            plain_block = feistel(plain_block, get_subKey(key, i + 1))

        plain_block = plain_block[int(len(plain_block) / 2):] + plain_block[:int(len(plain_block) / 2)]

        IV = plain_block

        for b in block:
            temp += encode_B6(b)

        if counter <= len(blocks) - 2:
            plain_block = utilities.xor(plain_block, temp)
        else:
            plain_block = utilities.xor(temp, plain_block[:len(temp)])

        b_blocks = utilities.text_to_blocks(plain_block, 6)
        for b_b in b_blocks:
            plaintext += decode_B6(b_b)

        counter += 1

    plaintext = utilities.insert_undefinedList(plaintext, undefined)

    return plaintext
