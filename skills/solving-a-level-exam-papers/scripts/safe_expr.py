"""Whitelisted AST interpreter for check expressions. No eval/exec/sympify.

Threat model: checks.json is authored from PDF/user text, which is untrusted.
Only the node types, names and functions below can ever be evaluated.
"""
from __future__ import annotations
import ast
import sympy as sp

MAX_CHARS, MAX_NODES, MAX_POW = 2000, 600, 1000
MAX_MATRIX_DIM, MAX_INT_ARG = 64, 10_000
MAX_SEQ = MAX_MATRIX_DIM * MAX_MATRIX_DIM


class UnsafeExpression(ValueError):
    """Expression rejected by the whitelist."""


def _int(v, name, cap):
    if isinstance(v, bool) or not isinstance(v, (int, sp.Integer)):
        raise UnsafeExpression(f"{name} must be an integer")
    n = int(v)
    if n < 0 or n > cap:
        raise UnsafeExpression(f"{name} must be in 0..{cap}")
    return n


def _dims(rows, cols):
    if rows > MAX_MATRIX_DIM or cols > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"matrix dimensions exceed {MAX_MATRIX_DIM}")


def _eye(rows, cols=None):
    r = _int(rows, "eye rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "eye cols", MAX_MATRIX_DIM)
    return sp.eye(r, c)


def _zeros(rows, cols=None):
    r = _int(rows, "zeros rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "zeros cols", MAX_MATRIX_DIM)
    return sp.zeros(r, c)


def _ones(rows, cols=None):
    r = _int(rows, "ones rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "ones cols", MAX_MATRIX_DIM)
    return sp.ones(r, c)


def _matrix(*args):
    if len(args) == 1:
        arg = args[0]
        rows = getattr(arg, "rows", None)
        if rows is not None:
            _dims(rows, getattr(arg, "cols", rows))
        elif isinstance(arg, (list, tuple)):
            r = len(arg)
            if r > MAX_MATRIX_DIM:
                raise UnsafeExpression(f"matrix dimensions exceed {MAX_MATRIX_DIM}")
            cols = 0
            for row in arg:
                if isinstance(row, (list, tuple)):
                    cols = max(cols, len(row))
                else:
                    cols = max(cols, 1)
            _dims(r, cols)
        m = sp.Matrix(arg)
    elif len(args) == 3:
        r = _int(args[0], "Matrix rows", MAX_MATRIX_DIM)
        c = _int(args[1], "Matrix cols", MAX_MATRIX_DIM)
        if isinstance(args[2], (list, tuple)) and len(args[2]) > r * c:
            raise UnsafeExpression(f"Matrix data exceeds {r * c} entries")
        m = sp.Matrix(r, c, args[2])
    else:
        raise UnsafeExpression("Matrix expects 1 or 3 arguments")
    _dims(m.rows, m.cols)
    return m


def _det(m):
    return _matrix(m).det()


def _inv(m):
    return _matrix(m).inv()


def _transpose(m):
    return _matrix(m).T


def _diag(*args):
    if len(args) > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"diag exceeds {MAX_MATRIX_DIM} blocks")
    total = 0
    for a in args:
        rows = getattr(a, "rows", None)
        if rows is not None:
            total += max(rows, getattr(a, "cols", rows))
        elif isinstance(a, list):
            total += len(a)
        else:
            total += 1
    if total > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"diag dimensions exceed {MAX_MATRIX_DIM}")
    return sp.diag(*args)


def _factorial(n):
    return sp.factorial(_int(n, "factorial", MAX_INT_ARG))


def _binomial(n, k):
    return sp.binomial(_int(n, "binomial n", MAX_INT_ARG),
                       _int(k, "binomial k", MAX_INT_ARG))


def _gamma(z):
    if not getattr(z, "is_number", False):
        raise UnsafeExpression("gamma requires a numeric argument")
    try:
        value = sp.N(z)
        mag = abs(complex(value)) if not value.is_real else abs(float(value))
    except (TypeError, ValueError, OverflowError):
        raise UnsafeExpression("gamma argument is not finite") from None
    if not (mag <= MAX_INT_ARG):
        raise UnsafeExpression(f"gamma argument exceeds {MAX_INT_ARG}")
    return sp.gamma(z)


FUNCS = {
    "sqrt": sp.sqrt, "Abs": sp.Abs, "exp": sp.exp, "log": sp.log,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc,
    "cot": sp.cot, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "atan2": sp.atan2, "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "asinh": sp.asinh, "acosh": sp.acosh, "atanh": sp.atanh,
    "floor": sp.floor, "ceiling": sp.ceiling, "sign": sp.sign, "Mod": sp.Mod,
    "Min": sp.Min, "Max": sp.Max, "gcd": sp.gcd, "lcm": sp.lcm,
    "Rational": sp.Rational, "Integer": sp.Integer, "Matrix": _matrix,
    "diag": _diag, "eye": _eye, "zeros": _zeros, "ones": _ones,
    "det": _det, "inv": _inv, "transpose": _transpose,
    "conjugate": sp.conjugate, "re": sp.re, "im": sp.im, "arg": sp.arg,
    "factorial": _factorial, "binomial": _binomial, "gamma": _gamma,
    "simplify": sp.simplify, "expand": sp.expand, "factor": sp.factor,
    "cancel": sp.cancel, "together": sp.together, "trigsimp": sp.trigsimp,
    "ratsimp": sp.ratsimp, "diff": sp.diff, "integrate": sp.integrate,
    "limit": sp.limit, "discriminant": sp.discriminant, "solve": sp.solve,
}
CONSTS = {"pi": sp.pi, "E": sp.E, "I": sp.I, "oo": sp.oo}
BINOPS = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
          ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b}


def _ev(node, env):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise UnsafeExpression(f"constant type not allowed: {node.value!r}")
        return sp.Integer(node.value) if isinstance(node.value, int) else sp.Float(node.value)
    if isinstance(node, ast.Name):
        if node.id.startswith("_"):
            raise UnsafeExpression("names beginning with '_' are forbidden")
        if node.id in env:
            return env[node.id]
        raise UnsafeExpression(f"unknown name: {node.id}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        v = _ev(node.operand, env)
        return v if isinstance(node.op, ast.UAdd) else -v
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Pow):
            if any(isinstance(n, ast.Pow) for n in ast.walk(node.right)):
                raise UnsafeExpression("nested powers are forbidden")
            base, ex = _ev(node.left, env), _ev(node.right, env)
            if ex.is_number:
                try:
                    magnitude = abs(float(sp.N(ex)))
                except (TypeError, ValueError, OverflowError):
                    raise UnsafeExpression("non-finite exponent") from None
                # Compared outside the try: UnsafeExpression is a ValueError and
                # would otherwise be re-labelled "non-finite exponent".
                if magnitude > MAX_POW:
                    raise UnsafeExpression("exponent too large")
            return base ** ex
        if isinstance(node.op, ast.BitXor):
            raise UnsafeExpression("'^' is not supported; use '**' for powers")
        if isinstance(node.op, ast.Mult):
            left, right = _ev(node.left, env), _ev(node.right, env)
            if isinstance(left, (list, tuple)) or isinstance(right, (list, tuple)):
                seq, count = ((left, right) if isinstance(left, (list, tuple))
                              else (right, left))
                if isinstance(count, bool) or not isinstance(count, (int, sp.Integer)):
                    raise UnsafeExpression("sequence repetition requires an integer")
                n = int(count)
                if n > 0 and len(seq) * n > MAX_SEQ:
                    raise UnsafeExpression(f"sequence exceeds {MAX_SEQ} elements")
                return seq * n
            return left * right
        if isinstance(node.op, ast.Add):
            left, right = _ev(node.left, env), _ev(node.right, env)
            if (isinstance(left, (list, tuple)) and
                    isinstance(right, (list, tuple)) and
                    len(left) + len(right) > MAX_SEQ):
                raise UnsafeExpression(f"sequence exceeds {MAX_SEQ} elements")
            return left + right
        op = BINOPS.get(type(node.op))
        if op is None:
            raise UnsafeExpression(f"operator not allowed: {type(node.op).__name__}")
        return op(_ev(node.left, env), _ev(node.right, env))
    if isinstance(node, ast.Call):
        if node.keywords or any(isinstance(a, ast.Starred) for a in node.args):
            raise UnsafeExpression("keyword/starred arguments are forbidden")
        if not isinstance(node.func, ast.Name) or node.func.id not in FUNCS:
            raise UnsafeExpression("only whitelisted function names may be called")
        return FUNCS[node.func.id](*[_ev(a, env) for a in node.args])
    if isinstance(node, (ast.List, ast.Tuple)):
        if len(node.elts) > MAX_SEQ:
            raise UnsafeExpression(f"sequence exceeds {MAX_SEQ} elements")
        return [_ev(e, env) for e in node.elts]
    raise UnsafeExpression(f"node not allowed: {type(node).__name__}")


def parse(text, symbols=()):
    """Interpret `text` into a SymPy object using the whitelist only."""
    if not isinstance(text, str) or not text.strip():
        raise UnsafeExpression("expression must be a non-empty string")
    if len(text) > MAX_CHARS:
        raise UnsafeExpression(f"expression exceeds {MAX_CHARS} characters")
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise UnsafeExpression(f"syntax error: {exc.msg}") from None
    if sum(1 for _ in ast.walk(tree)) > MAX_NODES:
        raise UnsafeExpression(f"expression exceeds {MAX_NODES} nodes")
    env = dict(CONSTS)
    for s in symbols:
        if not isinstance(s, str) or not s.isidentifier() or s.startswith("_"):
            raise UnsafeExpression(f"invalid symbol name: {s!r}")
        if s in FUNCS or s in CONSTS:
            raise UnsafeExpression(f"symbol shadows a reserved name: {s}")
        env[s] = sp.Symbol(s)
    try:
        return _ev(tree.body, env)
    except UnsafeExpression:
        raise
    except (TypeError, AttributeError, sp.SympifyError) as exc:
        raise UnsafeExpression(f"ill-typed expression: {exc}") from None


def is_inexact(expr) -> bool:
    """True if a floating-point atom appears (banned in exact checks)."""
    return bool(getattr(expr, "atoms", lambda *_: set())(sp.Float))
