"""`KindId`: the `<ns>.<name>/<n>` identifier that ties an artifact to its schema.

`/0` is provisional (it may change without a migration); `/1` and above are stable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# DDD invariant 1. Explicit ASCII ranges, so no Unicode letters or digits slip in.
PATTERN = r"^[a-z][a-z0-9]*\.[a-z][a-z0-9_.]*/(0|[1-9][0-9]*)$"
_REGEX = re.compile(PATTERN)


class KindIdError(ValueError):
    """A text that is not a valid `KindId`. `code` is the catalog key, `text` the rejected input."""

    def __init__(self, code: str, text: object, reason: str) -> None:
        super().__init__(f"{reason}: {text!r}")
        self.code = code
        self.text = text


@dataclass(frozen=True, order=True)
class KindId:
    namespace: str
    name: str
    version: int

    def __post_init__(self) -> None:
        # Building one by hand goes through the same rule as parsing.
        if not isinstance(self.version, int) or isinstance(self.version, bool):
            raise KindIdError("kind_id.format", self.version, "version is not an integer")
        text = f"{self.namespace}.{self.name}/{self.version}"
        parsed = KindId.parse(text)
        # `KindId("a.b", "c", 1)` joins to `a.b.c/1`, which parses as `a` + `b.c`: reject what does not round-trip.
        if (parsed.namespace, parsed.name, parsed.version) != (self.namespace, self.name, self.version):
            raise KindIdError("kind_id.format", text, "fields do not round-trip through the text form")

    @classmethod
    def parse(cls, text: object) -> KindId:
        """Return the `KindId` of `text`, or raise `KindIdError` saying why it is not one."""
        if not isinstance(text, str):
            raise KindIdError("kind_id.type", text, "kind id is not a string")
        # fullmatch, not `$`: `$` would accept a trailing newline.
        match = _REGEX.fullmatch(text)
        if match is None:
            raise KindIdError("kind_id.format", text, f"kind id does not match {PATTERN}")
        head, _, digits = text.rpartition("/")
        namespace, _, name = head.partition(".")
        try:
            version = int(digits)
        except ValueError:  # more digits than Python's int limit
            raise KindIdError("kind_id.format", text, "version has too many digits") from None
        kind = object.__new__(cls)
        object.__setattr__(kind, "namespace", namespace)
        object.__setattr__(kind, "name", name)
        object.__setattr__(kind, "version", version)
        return kind

    @staticmethod
    def is_valid(text: object) -> bool:
        try:
            KindId.parse(text)
        except KindIdError:
            return False
        return True

    @property
    def provisional(self) -> bool:
        """`/0` may change without a migration."""
        return self.version == 0

    @property
    def stable(self) -> bool:
        return self.version >= 1

    def next(self) -> KindId:
        """The `/n+1` of this kind: the target of its migration."""
        return KindId(self.namespace, self.name, self.version + 1)

    def __str__(self) -> str:
        return f"{self.namespace}.{self.name}/{self.version}"
