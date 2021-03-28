# PCSP Tools

Tools for checking identities in polymorphism minions. Mostly. CSP solver not provided.

Written in Python, and currently depends on the `pycosat` SAT-solver. Technically this can be easily switched to any other CSP-/SAT-solver.
The majority of the code are reductions between CSP, SAT, and Label Cover, which in practice, is an implementation of \[[BKO19], Section 3\].


## Installation


Apparently, pip can install from github:

```
python3 -m pip install git+https://github.com/jakub-oprsal/pcsptools
```


## Testing identities

The primary purpose of this code is to quickly check whether a certain polymorphism minion satisfies some set of minor/height 1 identities.

The function to test identities is `test_identities`. Takes four arguments: two structures: `A` and `B`, `identities`, and, optionally, an alternative `solver`. If no solver is provided, reduction to SAT and pycosat is used.
The identities are given as a label cover template. To ease the input, we provide a parser from a natural language `parse_identities`: each identity (or a link of  identities) is given as a separate argument.

A working example would look like this:

```python
from pcsptools import *

solutions = test_identities(
        affine(2), affine(2),
        parse_identities(
            "u(xxy) = u(xyx) = u(yxx) = d(xy)",
            "v(xxxy) = v(xxyx) = v(xyxx) = v(yxxx) = d(xy)"))

try:
    solution = next(solutions)
except StopIteration:
    print('No such polymorphisms!')
```


## Structures (and CSP instances)

Relational structures are stored as instances of the class `Structure`. Constructed by `Structure(domain, relation1, relation2, ...)`. Each of the relations is an iterator (list, set, tuple, etc.) of tuples of elements from domain. A few structures are pre-defined:

- `clique(n)` – the complete graph on `n` vertices.
- `cycle(n)` – the unoriented `n`-cycle graph.
- `ocycle(n)` – the oriented `n`-cycle graph.
- `nae(n, arity=3)` – the 'not all equal' relation on an `n` element set, i.e., the template for hypergraph `n` colouring.
- `onein(n)` – the generalisation of 1-in-3SAT of arity `n`, containing those Boolean tuples with exactly one 1.
- `loop(n, m, ...)` – the 'loop' of the given type, i.e., the structure on 1-element domain where all relations are non-empty.
- `affine(p)` – the affine equations over **Z**\_p with one relation for each *i* = 0, ..., *p* − 1 defined as *R\_i* = {(*x*, *y*, *z*) : *x* + *y* + *z* = *i* mod *p*}.
- `hornsat()` - the template of Horn-SAT with two ternary and two singleton unary relations. Note it is a function that construct a copy of the structure.

A CSP instance is a pair of structures of the same relational type.


## Identities

There are a few easy ways to construct minor conditions:

- `parse_identities(*identies)` – parses identities written in natural language, e.g., in form of strings as `'m(x, x, y) = m(y, x, x) = m(y, y, y)'`. The commas and spaces are optional. Variable symbols can also be numbers, function symbols can only be letters.
- `loop_condition(structure, names=(s_0, s_1, ...))` – this constructs the loop condition corresponding to the given structure. The optional argument `names` holds the names of the function symbols assigned to relations of the structure.
- using the `csp_to_lc` function. You will need to distill it from the output since the output is in a monad that takes care of decoding.

Natively, identities are represented as a label cover instance which is a pair `(variables, constraints)` where each of the variables is a pair `(name, domain_size)`, and each constraint is a pair `((u, v), pi)` where `u` and `v` are variable names, and `pi` is the relation defining the constraint —we assume that `pi` is a graph of function, if it's not you may encounter undocumented behaviour.


## Reductions

We provide reductions between CSP, label cover, and SAT. The goal is to allow encoding of a CSP instance into a SAT instance, so that we can use  external SAT-solvers to solve CSP instances.

A reduction is a function that:
 - inputs (`in_instance`)
 - returns an element of a monad that is constructed using `out_instance` and a `decode` function.

This monad is an object with two methods: `bind(reduction)` that is used to compose reduction, and `solve(solver)` that executes the decoding. I don't think this is a good place to explain monads, look into the code to find details (or read a book on programming in Haskell from where I am borrowing these tricks).

The reductions are:

- `csp_to_lc` – from CSP to label cover;
- `lc_to_sat` – from label cover to SAT;
- `indicator_structure` – from label cover to CSP. This reduction requires a CSP Template as the first argument.

We also provide a helper function `csp_solver(sat_solver)` which produces a CSP-solver from a SAT-solver. Note that a clause is encoded as a list of signed integers where negative sign encodes nagation of a variable, i.e., `(-1, 2, 4)` is the clause ¬*x*\_1 ∨ *x*\_2 ∨ *x*\_4. A solver is expected to be an iterator over solutions (preferably all of them).


## Thanks

Thanks to Michal Rolínek for forcing me to package this thing!


## References

\[BKO19\] Jakub Bulín, Andrei Krokhin, Jakub Opršal. Algebraic approach to promise constraint satisfaction, In *Proceedings of the 51st Annual ACM Symp. on the Theory of Computing (STOC 2019)*, [doi:10.1145/3313276.3316300](https://doi.org/10.1109/FOCS.2019.00076).

[BKO19]: https://doi.org/10.1109/FOCS.2019.00076
