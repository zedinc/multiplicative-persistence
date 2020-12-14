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
    assert lp7(14)                  # 14 = 2 * 7
    assert not lp7(77)              # 11 is largest prime
    assert not lp7(277777788888899) # prime factorization: 13 * 59 * 1699 * 213161503
    assert lp7(4996238671872)       # prime factorization: 2^19 * 3^4 * 7^6

def test_lp7f():
    assert lp7f(14)                  # 14 = 2 * 7
    assert not lp7f(77)              # 11 is largest prime
    assert not lp7f(277777788888899) # prime factorization: 13 * 59 * 1699 * 213161503
    assert lp7f(4996238671872)       # prime factorization: 2^19 * 3^4 * 7^6
