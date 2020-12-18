from conjecture import *

def test_streak():
    assert streak(54) == [54, 20]
    assert streak(345) == [345, 60]
    assert streak(277777788888899) == [277777788888899, 4996238671872, 438939648, 4478976, 338688, 27648, 2688, 768, 336, 54, 20]

def test_pm():
    assert pm(39) == 27

def test_candidates():
    assert list( candidates(345)) == [345, 354, 435, 453, 534, 543]

def test_fast_streak():
    assert fast_streak(54) == [54, 20]
    assert fast_streak(345) == [345, 60]
    assert fast_streak(277777788888899) == [277777788888899, 4996238671872, 438939648, 4478976, 338688, 27648, 2688, 768, 336, 54, 20]

def test_sift():
    assert sift(345) == []
    assert sift(435) == []
    assert sift(338688) == [338688]
    assert sift(888336) == [338688]

def test_lp7():
    lp7_checks(lp7)
    
def test_lp7f():
    lp7_checks(lp7f)
    
def test_lp7ff():
    lp7_checks(lp7ff)
    
def test_lp237():
    lp7_checks(lp237)

def test_prime_powers():
    assert prime_powers237(4478976) == (11,7,0)
    assert prime_powers237(49) == (0,0,2)

def lp7_checks(func):
    assert func(14)                  # 14 = 2 * 7
    for i in range(1,10):
        assert func(i)
    assert not func(11)              # smallest possible false
    assert func(5)                   # prime single digit
    assert func(4)                   # non-prime single digit
    assert func(49)                  # 49 = 7 * 7
    assert func(243)                 # 49 = 7 * 7
    assert not func(51)              # double-digit prime
    assert not func(2247337344)      # double-digit prime
    assert not func(77)              # 11 is largest prime
    assert not func(277777788888899) # prime factorization: 13 * 59 * 1699 * 213161503
    assert func(4996238671872)       # prime factorization: 2^19 * 3^4 * 7^6
