from __future__ import annotations


class PossibleNumber:
    def __init__(self, value: int, sign: bool | None) -> None:
        self._value = value
        self._sign = sign

    @property
    def accurate_value(self) -> int:
        return self._value if self._sign else 0

    @property
    def value(self) -> int:
        return 0 if self._sign is False else self._value

    @property
    def signed(self) -> bool:
        return self._sign is not None

    @property
    def sign(self) -> bool | None:
        return self._sign

    def set_sign(self, sign: bool) -> None:
        self._sign = sign

    def get_signed_number(self, sign: bool) -> PossibleNumber:
        return PossibleNumber(self._value, sign)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value}, {self._sign})"

    def __hash__(self) -> int:
        return hash((self._value, self._sign))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PossibleNumber) and self._value == other._value and self._sign == other._sign
