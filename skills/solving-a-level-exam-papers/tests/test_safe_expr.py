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
