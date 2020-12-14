from functools import reduce
from itertools import product
# from numba import jit, vectorize, cuda
from time import time
import numpy as np
from sympy.utilities.iterables import multiset_permutations
from math import log, factorial as f

pm = lambda n : reduce( int.__mul__ , map( int , list( str(n) ) ) )
sift = lambda seed: list( i for i in candidates(seed) if lp7(i) )

def streak(n):
    if n > 9:
        return [ n ] + streak( pm(n) )
    else:
        return []

def fast_streak(n):
    if '0' not in str(n) and n > 9:
        return [ n ] + streak( pm(n) )
    else:
        return []

def search( TWO, THREE, SEVEN ):
    size = TWO * THREE * SEVEN
    count = 0
    for seven, three, two in product( range(SEVEN), range(THREE), range(TWO) ):
        count += 1
        print( '\r({}, {}, {}) - {:.2%}'.format( two, three, seven, count/size ), end = '' )
        n = 2**two * 3**three * 7**seven
        if '0' not in str(n) and len( fast_streak(n) ) > 7:
            print( '\r({}, {}, {}) = {}'.format( two, three, seven , n ) )


# @vectorize(['int_(int_)'],target='cuda')
# def pmv(n):
    # j = 1
    # for i in list(str(n)):
        # j *= int(i)
    # return j

# @vectorize(['int_(int_)'],target='cuda')
# def streakv(n,length):
    # i = 0
    # while n > 9:
        # i += 1
        # n = pmv(n)
    # return i

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

def largest_prime_single_digit(n):
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

def lp7(n):      # largest prime is 7
    i = 2
    while i <= 7 and n != 1:
        if n % i:
            i += 1
        else:
            n //= i
    return n == 1

def candidates( seed, ones=0 ):
    # while True:
        for n in multiset_permutations( str(seed) ):
            yield int( '1' * ones + ''.join(n) )
        # seed += '1'

def onesies( TWO, THREE, SEVEN, limit=10 ):
    ones = 0
    while ones <= limit:
        for seed in building_sets( TWO, THREE, SEVEN ):
            count = 0
            ext = '1' * ones + seed
            if len(ext) <= 80:
                print( 'Exploring {}'.format( ext ) )
            else:
                print( 'Exploring {}'.format( ext[:77] + '...' ) )
            for seq in candidates(seed,ones):
                count += 1
                length = len(str(seq))
                if length <= 80:
                    print( '\r  {} - {:.2%}'.format( str(seq), count/complexity(str(seq)) ), end = '' )
                else:
                    print( '\r  {} - {:.2%}'.format( str(seq)[:77] + '...', count/complexity(str(seq)) ), end = '' )
                if lp7( int(seq) ):
                    print( '\r  {}          '.format(seq) )
            print()
        ones += 1

def unit(seed):
    print(seed)
    for i in candidates(seed):
        print( '\r' + i, end = '' )
        if lp7(i): print( '\r' + i )

def building_sets(TWO,THREE,SEVEN):
    n = 2 ** TWO * 3 ** THREE * 7 ** SEVEN
    assert lp7(n), 'Largest prime factor must be 7'
    
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

def sequence_summary(two,three,seven):
    score = {}
    for seq in building_sets(two,three,seven):
        # uniq = [ int(i) for i in set(seq) ]
        # count = { i : seq.count(str(i)) for i in uniq }
        # combinations = f(len(seq))
        # for i in uniq:
            # combinations //= f( count[i] )
        # score[seq] = combinations
        score[seq] = complexity(seq)
    return score


def prime_factors(n):
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

def prime_powers(n):
    assert lp7(n), "Can't use prime_powers() if largest prime > 7"
    factors = prime_factors(n)
    return factors.count(2), factors.count(3), factors.count(7)

def find_prospects( n, pad='', level=0 ):
    assert lp7(n), "Can't use find_prospects() if largest prime > 7"
    print( pad + str(n) )
    TWO, THREE, SEVEN = prime_powers(n)
    possibilities = sequence_summary( TWO, THREE, SEVEN )
    for _, score in sorted( possibilities.items(), key = lambda x: x[1] ):
        print('\r' + pad + '  {}'.format(_))
        for seq in candidates(_):
            print( '\r' + pad + '* {}'.format(seq), end='')
            i = int(seq)
            if lp7(i) and i != n:
                two, three, seven = prime_powers(i)
                print( '\r' + pad + '  {} = 2**{} * 3**{} * 7**{}'.format( seq, two, three, seven ) )
                if level > 0:
                    find_prospects( i, pad+'  ' )

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
    
    onesies( 4, 20, 5, 2 )
