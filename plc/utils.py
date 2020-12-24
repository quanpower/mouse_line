
def bcd_to_int(x):
    """
    This translates binary coded decimal into an integer
    TODO - more efficient algorithm
    >>> bcd_to_int(4)
    4
    >>> bcd_to_int(159)
    345
    """

    if x < 0:
        raise ValueError("Cannot be a negative integer")

    binstring = ''
    while True:
        q, r = divmod(x, 10)
        nibble = bin(r).replace('0b', "")
        while len(nibble) < 4:
            nibble = '0' + nibble
        binstring = nibble + binstring
        if q == 0:
            break
        else:
            x = q

    return int(binstring, 2)


def int_to_bcd(x):
    """
    This translates an integer into
    binary coded decimal
    >>> int_to_bcd(4)
    4
    >>> int_to_bcd(34)
    22
    
    >>> int_to_bcd(0)
    0
    """

    if x < 0:
        raise ValueError("Cannot be a negative integer")
        
    if x == 0:
        return 0
        
    bcdstring = ''
    while x > 0:
        nibble = x % 16
        bcdstring = str(nibble) + bcdstring
        x >>= 4
    return int(bcdstring)


def bcd2time(x):
    return int(x[0:4], 2)*10 + int(x[4:8], 2)


def byte2string(x):
    return 'xx'


def checksum(x):
    cs = 0
    for i in range(len(x)):
        cs = cs + x[i]
    # print(cs%256)
    return cs%256


def num2bcd(num):
    a = (num % 10) & 0x0f
    print(a)
    b = ((num // 10) << 4) & 0xf0
    bcd = a | b
    return bcd


# def int2bitarray_8(int_, length):
#     a=  bin(int_)
#     b = a[2:]
#     c= [i for i in b]
#     if len(c) < length:
#         c = extend_list(c, length)
#     d = [True if i == '1' else False for i in c]
#     e = d[::-1]

#     return e

# def int2bitarray_16(int_, length):
#     a=  bin(int_)
#     b = a[2:]
#     c= [i for i in b]
#     if len(c) < length:
#         c = extend_list(c, length)
#     d = [True if i == '1' else False for i in c]
#     e = d[::-1]
#     print(e)
#     f = e[-8:].extend(e[0:8])
#     print(f)
#     return f 

# def int2bitarray_32(int_, length):
#     a=  bin(int_)
#     b = a[2:]
#     c= [i for i in b]
#     if len(c) < length:
#         c = extend_list(c, length)
#     d = [True if i == '1' else False for i in c]
#     e = d[::-1]
#     f = e[-8:].extend(e[0:8])
#     return f 





# def extend_list(list_, length):
#     d = ['0' for i in range(length-len(list_))]
#     d.extend(list_)
#     return d


def int2bitarray(int_, length):
    try:
        a =int_
        b=[]
        while 1:
            c,d = divmod(a,2)
            a = c
            b.append(d)
            if c < 2:
                b.append(c)
                break

        if len(b) < length:
            d = [0 for i in range(length-len(b))]
            b.extend(d)

        # print('---len(b)----')
        # print(len(b))
        # print(b)

        if length <=8:
            return true_false_0_1(b)

        elif length > 8 and length <=16:
            e = b[8:]
            e.extend(b[0:8])
            return true_false_0_1(b)

        elif length >16 and length <= 32:
            f = b[0:8]
            g = b[8:16]
            h = b[16:24]
            i = b[24:32]

            f.extend(g)
            f.extend(h)
            f.extend(i)

            return true_false_0_1(b)

    except  Exception as e:
        pass
        
def true_false_0_1(list_):
    return [True if i == 1 else False for i in list_]


