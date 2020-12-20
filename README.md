# Multiplicative Persistence

Exploratory work inspired by [Numberphile video][1] on the topic.

---

![Multiplicative Peristence Graph][graph]

---

Some serious thought went into reducing the search effort as much as possible:

1. Search space expressed in terms of three variables, `TWO`, `THREE` & `SEVEN` (since all numbers of interest can be expressed as `2**TWO * 3**THREE * 7**SEVEN`).

   Technically `5**FIVE` can also be part of the definition but initial testing suggests the likelihood of finding something meaningful is extremely, extremely low for the cost of the additional dimension (if `5` and another even number show up in the string, the next number's going to have a `0` in it)

2. Heuristics to reduce time being spent on dead-ends, like:
  - Numbers whose largest prime factor > `7` (`lp7` routine)
  - Numbers containing a `0` (`fast_streak`)

---

## Future Work

1. Speed up through effective memoization
1. Speed up through parallelization. I tried to use `numba` to parallelize execution but I'm not sure how I should decorate the functions to allow support for bigints
2. Find a number whose digits multiply to give the larger numbers like `277777788888899`. This is where the `onesies` concept comes in; interspersing one or more `1` can yield a solution whose largest prime factor is `7`

  [1]: https://youtu.be/Wim9WJeDTHQ
  [graph]: https://github.com/zedinc/multiplicative-persistence/blob/main/scripts/graph-generator/test.svg