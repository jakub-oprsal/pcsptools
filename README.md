# PCSP Tools

Tools for checking identities in polymorphism minions. Mostly. CSP solver is
provided through a hook to the [pycosat] solver (which itself is a package of
python binding for picosat CSP solver).

The package provides a bunch of reductions between CSP, SAT, Label Cover, and
satisfaction of minor Maltsev conditions which in practice, is an
implementation of \[[BKO19], Section 3\].


## Installation

Apparently, pip can install from github:
```
python3 -m pip install git+https://github.com/jakub-oprsal/pcsptools
```


## Usage

The primary purpose of this code is to quickly check whether a certain
polymorphism minion satisfies some set of minor/height 1 identities. Naturally,
it can also quickly look for polymorphisms, or solve CSPs where the instance is
given as a homomorphism problem.

The key input is the class Structure which represents a relational structure in
an object that can be used elsewhere. A structure is constructed, e.g., as
```python
oneinthree = Structure(
        (0, 1),
        ((0, 0, 1), (0, 1, 0), (1, 0, 0))
        )
```
Both domain and any of the relations can be given as iterator, i.e., the above
could be also written as
```python
oneinthree = Structure(
        range(2),
        (tuple((1 if i == k else 0) for i in range(3)) for k in range(3))
        )
```
There are a bunch of predefined structures; see below, or the file `structure.py`.

To find all polymorphisms, we can use the function
```python
polymorphisms(A, B, arity, solver=pyco_solver)
```
Which iterates through all polymorphisms from `A` to `B` of arity `arity`. The
optional argument gives an alternative CSP solver (e.g., if you want to find
all polymoprhisms to `B` with a tractable CSP, you might want to implement your
own solver for that).

Finally, for testing identities, we provide function `check_identities` with header
```python
check_identities(A, B, identities, solver=pyco_solver)
```
The arguments are hopefully self-explanatory. Identities are given as a label
cover instance, i.e., a list of variables given as pairs `(name, domain)` and a
list of constraints given as pair `((name1, name2), binary_relation)`.  To
produce such an instance, we provide a~few functions:
- `parse_identities(*strings)` that inputs identities as string in a natural
  language, example given below. Commas and spaces separating variables are
  optional, variable names cna be either letters, or digits, and functions
  names have to be ascii letters, e.g., `'m(x, x, y) = m(x, y, x) = m(y, x, x)'`
  and `'   s(123,123)=s(231,321) '`.
- `loop_condition(structure, names = ('s0', ...), vertex_name = 'i0')` that
  creates a loop condition from a structure, e.g., the 6-ary Siggers identity
  can be given as `loop_condition(clique(3), names = ('s'))`.
- `sigma(A, B)` that constructs a minor condition denoted by
  $\Sigma(\mathbb A, \mathbb B)$ in \[[BKO19], Section 3\], i.e., `sigma(A, loop)` is
  the loop condition, and `sigma(A, B)` is trivial iff `A` maps homomorphically
  to `B`.

A working example would look like this:

```python
solutions = check_identities(
        affine(2), affine(2),
        parse_identities(
            "u(xxy) = u(xyx) = u(yxx) = d(xy)",
            "v(xxxy) = v(xxyx) = v(xyxx) = v(yxxx) = d(xy)"))

try:
    solution = next(solutions)
    print(solution)
except StopIteration:
    print('No such polymorphisms!')
```
Can you guess the output?


## Structures

Finally, let me give a list of some implemented structures. To repeat myself,
you can construct more as instances of the class `Structure` as
`Structure(domain, relation1, relation2, ...)` where each of the relations is
an iterator (list, set, tuple, etc.) of tuples of elements from domain. The
predefined structures are:

- `clique(n)` – the complete graph on `n` vertices.
- `cycle(n)` – the unoriented `n`-cycle graph.
- `ocycle(n)` – the oriented `n`-cycle graph.
- `nae(n, arity=3)` – the 'not all equal' relation on an `n` element set, i.e.,
  the template for hypergraph `n` colouring.
- `onein(n)` – the generalisation of 1-in-3SAT of arity `n`, containing those
  Boolean tuples with exactly one 1.
- `tinn(t,n)` – the generalisation of the above, namely the Boolean `t`-in-`n`SAT.
- `loop(n, m, ..., name=0)` – the 'loop' of the given type, i.e., the structure
  on 1-element domain where all relations are non-empty. The optional argument
  gives a name to the the unique element of the structure.
- `affine(p, arity=3)` – the affine equations over $\mathbb Z_p$ where
  $p ={}$`p` with one relation for each $i = 0, \dots, p − 1$ defined asr
  $R_i = \\{(x, y, z) : x + y + z = i \bmod p\\}$.
- `hornsat()` - the template of Horn-SAT with two ternary and two singleton
  unary relations. Note it is a function that construct a copy of the
  structure.


## Reductions

We provide reductions between CSP, label cover, and SAT. The goal is to allow
encoding of a CSP instance into a SAT instance, so that we can use  external
SAT-solvers to solve CSP instances.  A CSP instance is a pair of structures of
the same relational type.

A reduction is a function that:
 - inputs (`in_instance`)
 - returns an element of a monad that is constructed using `out_instance` and a
   `decode` function.

This monad is an object with two methods: `bind(reduction)` that is used to
compose reduction, and `solve(solver)` that executes the decoding. I don't
think this is a good place to explain monads, look into the code to find
details (or read a book on programming in Haskell from where I am borrowing
these tricks).

The reductions are:

- `csp_to_lc` – from CSP to label cover;
- `lc_to_sat` – from label cover to SAT;
- `indicator_structure` – from label cover to CSP. This reduction requires a
  CSP Template as the first argument.

The module `solver.py` provides a hook for [pycosat] solver and a helper
function `csp_solver(sat_solver)` which produces a CSP-solver from a
SAT-solver. Note that a clause is encoded as a list of signed integers where
negative sign encodes nagation of a variable, i.e., `(-1, 2, 4)` is the clause
¬*x*\_1 ∨ *x*\_2 ∨ *x*\_4. A solver is expected to be an iterator over
solutions (preferably all of them).


## Contributing and feedback

If you find this package useful, I would be delighted to learn about it! There
are probably as many implementations of some kind of identity/polymoprhism
tester as they are coding-able scientists in the CSP community. Nevertheless, I
think we might benefit in joining our efforts, and there is a lot that can be
improved in this package! Feel free to raise an issue, or create a pull request
if you have coded any extension of these tools. Also, if you have energy and do
not know where to start, please get in touch here or by email! 


## Thanks

Thanks to Michal Rolínek for forcing me to package this thing!  I would also
like to link Antoine Mottet's [csptools] which is a package with very similar
purpose (though slightly more titlted towards CSPs) that I used as inspiration
for this one.


## References

\[BKO19\] Jakub Bulín, Andrei Krokhin, Jakub Opršal. Algebraic approach to
promise constraint satisfaction, In *Proceedings of the 51st Annual ACM Symp.
on the Theory of Computing (STOC 2019)*,
[doi:10.1145/3313276.3316300](https://doi.org/10.1109/FOCS.2019.00076).

[BKO19]: https://doi.org/10.1109/FOCS.2019.00076
[pycosat]: https://github.com/conda/pycosat
[csptools]: https://github.com/amottet/csptools
