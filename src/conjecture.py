from functools import reduce
from itertools import product
from math import factorial as f
from math import log
# from numba import jit, vectorize, cuda
from time import time

import numpy as np
from colors import green
from sympy.utilities.iterables import multiset_permutations

pm = lambda n : reduce( int.__mul__ , map( int , list( str(n) ) ) )
sift = lambda seed: list( i for i in candidates(seed) if lp7(i) )
N237 = lambda TWO, THREE, SEVEN: 2 ** TWO * 3 ** THREE * 7 ** SEVEN
N2357 = lambda TWO, THREE, FIVE, SEVEN: 2**TWO * 3**THREE * 5**FIVE * 7**SEVEN

def streak(n):
    """Returns the list of numbers corresponding to the multiplicative persistence of the input number `n`.
    Doesn't add numbers below 10 to the list."""
    if n > 9:
        return [ n ] + streak( pm(n) )
    else:
        return []

def fast_streak(n):
    "Faster version of `streak` as it terminates the moment a zero is found in the latest result"
    if '0' not in str(n) and n > 9:
        return [ n ] + streak( pm(n) )
    else:
        return []

def search( TWO, THREE, SEVEN, action=None ):
    size = TWO * THREE * SEVEN
    count = 0
    for seven, three, two in product( range(SEVEN), range(THREE), range(TWO) ):
        count += 1
        print( '\r({}, {}, {}) - {:.2%}'.format( two, three, seven, count/size ), end = '' )
        n = 2**two * 3**three * 7**seven
        # if '0' not in str(n) :
        if '0' not in str(n) and len( fast_streak(n) ) > 7:
            print( '\r({}, {}, {}) = {}'.format( two, three, seven , n ) )
            action(TWO,THREE,SEVEN)

def explorer(seed):
    queue = [ str(seed) ]
    while True:
        start = queue.pop(0)
        for new_digit in [ 7, 8, 9 ]:
            last_digit = str(start)[-1]
            if int(last_digit) <= int(new_digit):
                new_number = str(start) + str(new_digit)
                queue.append(new_number)
                yield new_number

def work(seed):
    for n in explorer(seed):
        length = len( streak( int(n) ) )
        if length > 7:
            print( '[{}] {} : {}'.format( seed, n, length ) )

def lp7ff(n):
    """True/false if the largest prime is 7. Requires fewer loops than lp7"""
    i = 2
    while True:
        if n % i:
            # print('In if  : {i}, {n}'.format(i=i,n=n))
            if   i == 2: i = 3
            elif i == 3: i = 5
            elif i == 5: i = 7
            elif i == 7: return False
        else:
            # print('In else: {i}, {n}'.format(i=i,n=n))
            n //= i
        if n == 1:
            # print('In n==1: {i}, {n}'.format(i=i,n=n))
            return True

def lp237(n):
    """True/false if the largest prime is at most 7. Requires fewer loops than lp7, bit-shifts to divide by 2 as much as possible"""
    
    # Get rid of all divide by 2's in one bit-shift line
    n >>= bin(( n ^ (n-1) ) >> 1).count('1')
    if n < 11: return True
    
    i = 3  # 'Skip' testing 3 if it isn't divisible
    while n >= 11:
        if n % i:
            if   i == 3: i = 7
            elif i == 7: return False
        else:
            n //= i
    return True

def lp27(n):
    """True/false if the largest prime is 7. Requires fewer loops than lp7, bit-shifts to divide by 2 as much as possible. Asserts that number input is not divisible by 3"""
    
    # assert n % 3, 'Number should not be divisible by 3'
    
    # Get rid of all divide by 2's in one bit-shift line
    n >>= bin(( n ^ (n-1) ) >> 1).count('1')
    if n < 11: return True
    
    while n >= 11:
        if n % 7:
            return False
        else:
            n //= 7
    return True
    
def lp7f(n):
    """True/false if the largest prime is 7. Requires fewer loops than lp7"""
    primes = [2,3,5,7,None]
    i = primes.pop(0)
    while len(primes):
        if n % i:
            # print('In if  : {i}, {n}'.format(i=i,n=n))
            i = primes.pop(0)
        else:
            # print('In else: {i}, {n}'.format(i=i,n=n))
            n //= i
        if n == 1:
            # print('In n==1: {i}, {n}'.format(i=i,n=n))
            return True
    return False

def lp7(n):
    """True/false if the largest prime is 7"""
    i = 2
    while i <= 7 and n != 1:
        if n % i:
            i += 1
        else:
            n //= i
    return n == 1

def candidates( seed, ones=0 ):
    """Returns all permutations of the digits of `seed`, in addition to any `1` digits that can be specified via optional `ones` argument"""
    for n in multiset_permutations( '1' * ones + str(seed) ):
        yield int( ''.join(n) )

def onesies( TWO, THREE, SEVEN, start=0, limit=10 ):
    ones = start
    while ones <= limit:
        for seed in building_sets( TWO, THREE, SEVEN ):
            # what is in the loop represents one computational unit
            ext = '1' * ones + seed
            
            if len(ext) <= 80:
                print( 'Exploring {}'.format( ext ) )
            else:
                print( 'Exploring {}'.format( ext[:77] + '...' ) )
            
            count = 0
            cmplx = complexity(ext)
            divisible_by_three = not ( sum([int(i) for i in ext]) % 3 )
            prospective = lp237 if divisible_by_three else lp27

            for seq in candidates(seed,ones):
                count += 1
                print( '\r  {} - {:.2%}'.format( str(seq), count/cmplx ), end = '' )
                # length = len(str(seq))
                # if length <= 80:
                #     print( '\r  {} - {:.2%}'.format( str(seq), count/cmplx ), end = '' )
                # else:
                #     print( '\r  {} - {:.2%}'.format( str(seq)[:77] + '...', count/cmplx ), end = '' )
                if prospective( int(seq) ):
                    print( green( '\r  {}          '.format(seq) ) )
            print()
        ones += 1

def unit(seed):
    print(seed)
    for i in candidates(seed):
        print( '\r' + i, end = '' )
        if lp7(i): print( '\r' + i )

def building_sets(TWO,THREE,SEVEN):
    """Constructs all digit sets for 2**`TWO` * 3**`THREE` * 7**`SEVEN` (without including `1`s)"""
    n = 2 ** TWO * 3 ** THREE * 7 ** SEVEN
    assert lp7f(n), 'Largest prime factor must be 7'
    
    options2 = []
    for two, four, eight in product( range( 1+int(TWO/1) ), range( 1+int(TWO/2) ), range( 1+int(TWO/3) ) ):
        # print( 'Two : ' + str(two), str(four), str(eight), sep = ', ' )
        if two * 1 + four * 2 + eight * 3 == TWO:
            options2.append( '2' * two + '4' * four + '8' * eight )
    
    options3 = []
    for three, nine in product( range( 1+int(THREE/1) ), range( 1+int(THREE/2) ) ):
        if three * 1 + nine * 2 == THREE:
            options3.append( '3' * three + '9' * nine )
    
    options7 = [ '7' * SEVEN ]
    
    # print( '# {}, {}, {} #'.format( options2, options3, options7 ) )
    # print(options3)
    # print(options7)
    # return ( two + three + seven for two, three, seven in product( options2, options3, options7 ) )
    
    for two, three, seven in product( options2, options3, options7 ):
        seq = two + three + seven
        yield seq
        
        two_count = two.count('2')
        three_count = three.count('3')
        if two_count and three_count:
            for SIX in range( 1, 1 + min( two_count, three_count ) ):
                two_mod = '2' * ( two_count - SIX ) + two.strip('2')
                three_mod = '3' * ( three_count - SIX ) + three.strip('3')
                alt_seq = two_mod + three_mod + '6' * SIX + '7' * SEVEN
                # print( 'alt_seq = {}'.format(alt_seq) )
                if alt_seq != seq:
                    yield alt_seq

def complexity(seq):
    uniq = [ int(i) for i in set(str(seq)) ]
    count = { i : seq.count(str(i)) for i in uniq }
    complexity = f(len(seq))
    for i in uniq:
        complexity //= f( count[i] )
    return complexity

def sequence_summary(TWO,THREE,SEVEN):
    """Returns a dictionary summarizing the different digit sets that satisfy the prime factorization of 2**`TWO` * 3**`THREE` * 7**`SEVEN`.
    :param two: number of times 2 repeats as a prime factor
    :param three: number of times 3 repeats as a prime factor
    :param seven: number of times 7 repeats as a prime factor
    """
    score = {}
    for seq in building_sets(TWO,THREE,SEVEN):
        # uniq = [ int(i) for i in set(seq) ]
        # count = { i : seq.count(str(i)) for i in uniq }
        # combinations = f(len(seq))
        # for i in uniq:
            # combinations //= f( count[i] )
        # score[seq] = combinations
        score[seq] = complexity(seq)
    return score

def prime_factors(n):
    """Returns list of prime factors for `n`"""
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def prime_powers237(n):
    """Returns `TWO`, `THREE`, `SEVEN` representation of `n` (2**`TWO` * 3**`THREE` * 7**`SEVEN`)"""
    assert not set(prime_factors(n)).difference({2,3,7}), "`prime_powers237()` only works if prime factors are limited to 2,3 and 7"
    factors = prime_factors(n)
    return factors.count(2), factors.count(3), factors.count(7)

def prime_powers2357(n):
    """Returns `TWO`, `THREE`, `FIVE`, `SEVEN` representation of `n` (2**`TWO` * 3**`THREE` * 5**`FIVE` * 7**`SEVEN`)"""
    assert not set(prime_factors(n)).difference({2,3,5,7}), "`prime_powers237()` only works if prime factors are limited to 2,3 and 7"
    factors = prime_factors(n)
    return factors.count(2), factors.count(3), factors.count(5), factors.count(7)

def find_prospectives( n, pad='', level=0 ):
    assert lp7(n), "Can't use find_prospectives() if largest prime > 7"
    print( pad + str(n) )
    TWO, THREE, SEVEN = prime_powers237(n)
    possibilities = sequence_summary( TWO, THREE, SEVEN )
    for _, score in sorted( possibilities.items(), key = lambda x: x[1] ):
        print('\r' + pad + '  {}'.format(_))
        for seq in candidates(_):
            print( '\r' + pad + '* {}'.format(seq), end='')
            i = int(seq)
            if lp7(i) and i != n:
                two, three, seven = prime_powers237(i)
                print( '\r' + pad + '  {} = 2**{} * 3**{} * 7**{}'.format( seq, two, three, seven ) )
                if level > 0:
                    find_prospectives( i, pad+'  ' )

if __name__ == '__main__':
    # for n in explorer():
        # length = len( streak( int(n) ) )
        # if length > 7:
            # print( '[{}] {} : {}'.format( n, length ) )
    
    # tic = time()
    # sequential
    # for seven, three, two in product( range(500), range(500), range(500) ):
        # n = 2**two * 3**three * 7**seven
        # if not str(n).count('0'):
            # length = len( streak(n) )
            # print( '\r({}, {}, {}) = '.format(two, three, seven), end='')
            # if length > 7: print( n, length, sep=': ')
    # toc = time()
    # print('Time taken = {} s'.format(toc-tic))
    
    # tic = time()
    # # parallelized?
    # for seven, three, two in product( range(100), range(100), range(100) ):
        # n = 2**two * 3**three * 7**seven
        # if not str(n).count('0'):
            # nv = streakv(n)
            # print( '\r({}, {}, {}) = '.format(two, three, seven), end='')
            # if nv > 7: print( n, nv, sep=': ')
    # toc = time()
    # print('Time taken = {} s'.format(toc-tic))
    
    # for i in candidates('54'):
        # print('\r' + str(i), lp7(i), sep = ': ' , end = '')
        # if lp7(i): print( '\r'+ str(i), lp7(i), sep = ':  ' )
    
    # print( complexity('1234') )
    
    # ones = 0
    # while ones <= 3:
        # for seed in building_sets( 4, 20, 5 ):
            # count = 0
            # for seq in candidates(seed,ones):
                # count += 1
                # print( '\r{} digits - {:.2%}'.format( len(str(seq)), count/complexity(str(seq)) ), end = '' )
                # if lp7( int(seq) ): print( '\r{}'.format(seq) )
            # print()
        # ones += 1

    # search( 40, 40, 40 )
    # exit(0)
    # onesies( 4, 20, 5, 5 )
    onesies( 8, 3, 2, 5 )
