"""Canonical JSON (RFC 8785, JCS) and content hashes, stdlib only.

DDD invariants 9 and 14. Own input restrictions on top of JCS: integers and floats outside +-(2^53-1), `NaN`, `Infinity`,
`-0` and duplicate object keys are rejected. `loads_strict` reads with those rules; `canonical_bytes` enforces
the same on a Python value.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from typing import Any

MAX_SAFE_INT = 2**53 - 1
_ESCAPES = {'"': '\\"', "\\": "\\\\", "\b": "\\b", "\t": "\\t", "\n": "\\n", "\f": "\\f", "\r": "\\r"}


class CanonError(ValueError):
    """A value or text the canon rejects. `code` is the stable catalog key; `path` is a JSON Pointer or ""."""

    def __init__(self, code: str, reason: str, path: str = "") -> None:
        super().__init__(f"{reason} at {path!r}" if path else reason)
        self.code = code
        self.path = path


def _check_int(value: int, path: str = "") -> int:
    if abs(value) > MAX_SAFE_INT:
        raise CanonError("canon.int_range", f"integer outside +-(2^53-1): {value}", path)
    return value


def _check_float(value: float, path: str = "") -> float:
    if math.isnan(value):
        raise CanonError("canon.nan", "NaN is not allowed", path)
    if math.isinf(value):
        raise CanonError("canon.infinity", "infinity is not allowed (or the number overflows a double)", path)
    if value == 0 and math.copysign(1.0, value) < 0:
        raise CanonError("canon.negative_zero", "negative zero is not allowed", path)
    if abs(value) > MAX_SAFE_INT:
        raise CanonError("canon.int_range", f"number outside +-(2^53-1): {value!r}", path)
    return value


def _parse_int(text: str) -> int:
    if len(text.lstrip("-")) > 16:
        raise CanonError("canon.int_range", f"integer outside +-(2^53-1): {text[:20]}...")
    value = int(text)
    if value == 0 and text.startswith("-"):
        raise CanonError("canon.negative_zero", "negative zero is not allowed: -0")
    return _check_int(value)


def _parse_float(text: str) -> float:
    return _check_float(float(text))


def _parse_constant(name: str) -> Any:
    code = "canon.nan" if name == "NaN" else "canon.infinity"
    raise CanonError(code, f"{name} is not allowed")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonError("canon.duplicate_key", f"duplicate object key {key!r}")
        result[key] = value
    return result


def loads_strict(text: str) -> Any:
    """Parse JSON `text`, rejecting duplicate keys, NaN/Infinity, -0 and out-of-range numbers."""
    if not isinstance(text, str):
        raise CanonError("canon.type", f"text is not a string: {type(text).__name__}")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_constant=_parse_constant,
            parse_int=_parse_int,
            parse_float=_parse_float,
        )
        _check_strings(value)
        return value
    except json.JSONDecodeError as exc:
        raise CanonError("canon.syntax", f"invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})") from None
    except RecursionError:
        raise CanonError("canon.syntax", "JSON nested too deeply") from None


def _number(value: float) -> str:
    """ECMAScript Number.prototype.toString for a finite, non-negative-zero double."""
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    mantissa, _, exp = repr(abs(value)).partition("e")
    whole, _, frac = mantissa.partition(".")
    if frac == "0":
        frac = ""
    digits = (whole + frac).lstrip("0")
    # value = 0.DIGITS x 10^n, with DIGITS the shortest round-trip digits (repr, like ES).
    n = len(whole) + (int(exp) if exp else 0)
    if whole == "0":
        n -= len(frac) - len(frac.lstrip("0")) + 1
    digits = digits.rstrip("0")
    k = len(digits)
    if k <= n <= 21:
        out = digits + "0" * (n - k)
    elif 0 < n <= 21:
        out = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        out = "0." + "0" * -n + digits
    else:
        e = n - 1
        out = digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + ("+" if e >= 0 else "-") + str(abs(e))
    return sign + out


def _check_utf8(text: str, path: str) -> None:
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        raise CanonError("canon.type", "string has a lone surrogate (not valid UTF-8)", path) from None


def _check_strings(value: Any) -> None:
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            _check_utf8(item, "")
        elif isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, dict):
            for key, child in item.items():
                _check_utf8(key, "")
                stack.append(child)


def _string(text: str, path: str) -> str:
    _check_utf8(text, path)
    out = []
    for ch in text:
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif ch < " ":
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def _emit(value: Any, path: str) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(_check_int(value, path))
    if isinstance(value, float):
        return _number(_check_float(value, path))
    if isinstance(value, str):
        return _string(value, path)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(_emit(item, f"{path}/{i}") for i, item in enumerate(value)) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise CanonError("canon.type", f"object key is not a string: {key!r}", path)
        parts = []
        for key in sorted(value, key=lambda k: k.encode("utf-16-be", "surrogatepass")):
            escaped = key.replace("~", "~0").replace("/", "~1")
            parts.append(_string(key, path) + ":" + _emit(value[key], f"{path}/{escaped}"))
        return "{" + ",".join(parts) + "}"
    raise CanonError("canon.type", f"not a JSON type: {type(value).__name__}", path)


def canonical_bytes(obj: Any) -> bytes:
    """The RFC 8785 (JCS) UTF-8 bytes of `obj`, or `CanonError` saying why it is not canonicalizable."""
    try:
        return _emit(obj, "").encode("utf-8")
    except RecursionError:
        raise CanonError("canon.type", "value nested too deeply (or cyclic)") from None


def content_hash(obj: Any) -> str:
    """`sha256:<hex>` of the canonical bytes of `obj` without its top-level `meta` (invariant 14)."""
    if isinstance(obj, dict):
        obj = {k: v for k, v in obj.items() if k != "meta"}
    return "sha256:" + hashlib.sha256(canonical_bytes(obj)).hexdigest()


def file_hash(path: str | os.PathLike[str]) -> str:
    """`sha256:<hex>` of the bytes of the file at `path`, as they are."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()
