import pytest
sp = pytest.importorskip("sympy")
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from safe_expr import UnsafeExpression, is_inexact, parse  # noqa: E402

PAYLOADS = [
    "__import__('os').system('echo pwned')",
    "().__class__.__mro__[1].__subclasses__()",
    "open('/tmp/x','w')", "eval('1+1')", "exec('x=1')",
    "(lambda: 1)()", "[x for x in (1,)]", "{'a':1}",
    "pi.__class__", "sqrt(2).__class__", "9**9**9", "2**100000",
    "_secret", "x^2", "Rational(1,2).__class__",
]


@pytest.mark.parametrize("src", PAYLOADS)
def test_payloads_rejected(src):
    with pytest.raises(UnsafeExpression):
        parse(src, symbols=("x",))


def test_exact_arithmetic_is_rational():
    e = parse("7/5 + sqrt(14)**2", symbols=())
    assert e == sp.Rational(7, 5) + 14
    assert not is_inexact(e)


def test_float_detected():
    assert is_inexact(parse("0.5 + 1"))


def test_unknown_name_rejected():
    with pytest.raises(UnsafeExpression):
        parse("mystery(1)")


@pytest.mark.parametrize("src", [
    "eye(65)", "zeros(65,65)", "ones(65,1)", "Matrix(65, 1, [0])",
    "factorial(10001)", "binomial(10001,2)", "gamma(10001)",
    "diag(eye(64), eye(64))", "[0]*4097", "Matrix([0]*65)",
    "Matrix([[0]*65]*65)", "Matrix(64, 64, [0]*4097)",
    "det([[0]*4096]*4096)", "inv([[0]*1000]*1000)",
    "transpose([[0]*1000]*1000)", "det([0]*4096)",
])
def test_oversized_allocations_rejected(src):
    with pytest.raises(UnsafeExpression):
        parse(src, symbols=("x",))


@pytest.mark.parametrize("src", [
    "eye(64)", "zeros(64,64)", "ones(64,1)", "Matrix([[1,2],[3,4]])",
    "factorial(1000)", "binomial(1000,2)", "gamma(100)", "diag(1,2,3)",
    "[0]*4096", "Matrix([0]*64)", "Matrix([[0]*64]*64)",
    "Matrix(64, 64, [0]*4096)",
])
def test_bounded_allocations_allowed(src):
    parse(src, symbols=("x",))
