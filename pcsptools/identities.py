'''
IDENTITIES

Tools to check height 1 identities in polymorphism minions.

The key construction ere is the *indicator structure* which creates the
instance of CSP whose solutions correspond to the solutions of the given
identities.

In addition, we have two helper tools: `Components` (which solves equality
CSP) and `parse_identities` which converts simply written identities into an
instance of label cover.
'''
from itertools import product, count
from .structure import product_relation, transpose, Structure
from .reductions import DelayDecode, csp_solver
import string


try:
    assert(default_solver is not None)
except (NameError, AssertionError):
    from pycosat import itersolve
    default_solver = csp_solver(itersolve)


class Components:
    """ a data structure holding connected components of a graph """

    def __init__(self, domain):
        self.tree = {a: a for a in domain}

    def __call__(self, a):
        """ returns the current representative from the same class as `a` """
        cur, same_as = a, ()
        while self.tree[cur] != cur:
            cur, same_as = self.tree[cur], same_as + (cur,)
        for e in same_as:
            self.tree[e] = cur
        return cur

    @property
    def domain(self):
        return iter(self.tree)

    def add(self, a, b):
        """ add an edge to the graph possibly collapsing two components"""
        self.tree[self(a)] = self(b)

    def items(self):
        """ iterates through pairs (a, representive of a/~) """
        return ((a, self(a)) for a in self.domain)

    def __iter__(self):
        """ iterates through representatives of the classes """
        return (a for a in self.tree if self.tree[a] == a)


def cover(domain, edges):
    """ Yields from a subset of vertices so that each other vertex is reachable
        from this set.  This is based on Kosaraju's algorithm for strongly
        connected components."""

    neighbours = {v: [] for v in domain}
    for u, v in edges:
        neighbours[u].append(v)

    to_visit, stack = set(domain), list()

    def build_stack(v):
        if v not in to_visit:
            return
        to_visit.remove(v)

        for u in neighbours[v]:
            build_stack(u)
        stack.append(v)

    for v in domain:
        build_stack(v)

    def remove_reachable(v):
        for u in neighbours[v]:
            if u in stack:
                stack.remove(u)
                remove_reachable(u)

    while True:
        try:
            v = stack.pop()
            yield v
            remove_reachable(v)
        except IndexError:
            return


def indicator_structure(Template, LC_instance):
    """ given a Template A and a LC instance Sigma
        builds the indicator structure of Sigma over A
        and passes the identification object """
    in_vars, in_cons = LC_instance

    # Construct the domain of the indicator by factoring
    arities = dict(in_vars)
    domain = ((f, x)
        for f, arity in arities.items()
        for x in product(Template.domain, repeat=arity))
    identify = Components(domain)
    for scope, relation in in_cons:
        f, g = scope
        pi = {x: y for x, y in relation}
        for x in product(Template.domain, repeat=arities[g]):
            x_pi = tuple(x[pi[i]] for i in range(arities[f]))
            identify.add((f, x_pi), (g, x))

    variables = iter(identify)

    # impose constraints that cover all thats necessary
    important_fs = tuple(cover(arities, (scope for scope, rel in in_cons)))

    def indicator_relation(template_relation):
        return set(
            tuple(identify((f, x)) for x in xs)
            for f in important_fs
            for xs in product_relation(template_relation, repeat=arities[f]))

    rels = (indicator_relation(relation) for relation in Template.relations)

    def decode(homomorphism):
        polymorphisms = dict()
        for f, arity in arities.items():
            polymorphisms[f] = {
                x: homomorphism[identify((f, x))]
                for x in product(Template.domain, repeat=arity)}
        return polymorphisms

    return DelayDecode(Structure(variables, *rels), decode)


def test_identities(A, B, identities, solver=default_solver):
    def cspB_solver(instance):
        yield from solver(instance, B)
    yield from indicator_structure(A, identities).solve(cspB_solver)


def parse_identities(*args):
    """ parses identities from strings to an LC instance:
        each arg contains a bunch of linked identities, e.g.
        'm(x, x, y) = m(x, y, x) = m(y, x, x)', or
        '   s(123,123)=s(231,321) """
    fs, constraints = dict(), list()

    for id_no, line in enumerate(args):
        terms, xs = [], set()
        state, fargs = 1, ""
        for i, char in enumerate(line):
            if state == 0:
                if char == ' ':
                    continue
                if char == '=':
                    state = 1
                else:
                    raise SyntaxError(
                        f"Unexpected character '{char}' at {id_no}:{i}.")
            elif state == 1:
                if char in " ":
                    continue
                if char in string.ascii_letters:
                    f = char
                    state = 2
                else:
                    raise SyntaxError(
                        f"Unexpected character '{char}' at {id_no}:{i}.")
            elif state == 2:
                if char == ' ':
                    continue
                if char == '(':
                    state = 3
            elif state == 3:
                if char in " ,":
                    continue
                if char in string.ascii_letters or char in string.digits:
                    fargs += char
                    xs.add(char)
                elif char == ")":
                    if len(fargs) == 0:
                        raise SyntaxError(
                            f"Unexpected character '{char}' at {id_no}:{i}.")
                    if f in fs and fs[f] != len(fargs):
                        raise SyntaxError(
                            f"'{f}' has ambiguous arity.")
                    else:
                        fs[f] = len(fargs)
                    terms.append((f, fargs[:]))
                    fargs = ""
                    state = 0
                else:
                    raise SyntaxError(
                        f"Unexpected character '{char}' at {id_no}:{i}.")
        if state != 0 or len(terms) == 1:
            raise SyntaxError('Unexpected end of input.')

        fs[f'i{id_no}'] = len(xs)
        x_to_i = {x: i for i, x in enumerate(xs)}

        for f, fargs in terms:
            constraints.append((
                (f, f'i{id_no}'),
                tuple((i, x_to_i[x]) for i, x in enumerate(fargs))))

    return tuple(fs.items()), tuple(constraints)


def loop_condition(structure, names=None):
    """ generates the loop condition corresponding to the given struture """
    minor_name = 'i0'
    if names is None:
        names = map(lambda i: f's_{i}', count(0))

    fs = dict()
    fs[minor_name] = len(structure.domain) # the common minor

    inverse = {a: i for i, a in enumerate(structure.domain)}
    def projections(relation):
        return transpose(
            tuple((i, inverse[a]) for a in edge)
            for i, edge in enumerate(relation))

    constraints = []
    for name, relation in zip(names, structure.relations):
        fs[name] = len(relation)
        for pi in projections(relation):
            constraints.append(((name, minor_name), pi))

    return tuple(fs.items()), tuple(constraints)
