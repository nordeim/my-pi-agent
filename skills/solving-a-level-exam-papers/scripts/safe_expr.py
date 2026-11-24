"""Whitelisted AST interpreter for check expressions. No eval/exec/sympify.

Threat model: checks.json is authored from PDF/user text, which is untrusted.
Only the node types, names and functions below can ever be evaluated.
"""
from __future__ import annotations
import ast
import sympy as sp

MAX_CHARS, MAX_NODES, MAX_POW = 2000, 600, 1000


class UnsafeExpression(ValueError):
    """Expression rejected by the whitelist."""


FUNCS = {
    "sqrt": sp.sqrt, "Abs": sp.Abs, "exp": sp.exp, "log": sp.log,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc,
    "cot": sp.cot, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "atan2": sp.atan2, "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "asinh": sp.asinh, "acosh": sp.acosh, "atanh": sp.atanh,
    "floor": sp.floor, "ceiling": sp.ceiling, "sign": sp.sign, "Mod": sp.Mod,
    "Min": sp.Min, "Max": sp.Max, "gcd": sp.gcd, "lcm": sp.lcm,
    "Rational": sp.Rational, "Integer": sp.Integer, "Matrix": sp.Matrix,
    "diag": sp.diag, "eye": sp.eye, "zeros": sp.zeros, "ones": sp.ones,
    "det": lambda m: sp.Matrix(m).det(), "inv": lambda m: sp.Matrix(m).inv(),
    "transpose": lambda m: sp.Matrix(m).T,
    "conjugate": sp.conjugate, "re": sp.re, "im": sp.im, "arg": sp.arg,
    "factorial": sp.factorial, "binomial": sp.binomial, "gamma": sp.gamma,
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
                    if abs(float(sp.N(ex))) > MAX_POW:
                        raise UnsafeExpression("exponent too large")
                except (TypeError, ValueError, OverflowError):
                    raise UnsafeExpression("non-finite exponent") from None
            return base ** ex
        if isinstance(node.op, ast.BitXor):
            raise UnsafeExpression("'^' is not supported; use '**' for powers")
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
    return _ev(tree.body, env)


def is_inexact(expr) -> bool:
    """True if a floating-point atom appears (banned in exact checks)."""
    return bool(getattr(expr, "atoms", lambda *_: set())(sp.Float))
