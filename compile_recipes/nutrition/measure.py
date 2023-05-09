from __future__ import annotations
from fractions import Fraction
from nutrition import units

class Measure:

    def __init__(self, arg, locked_in: bool | None = None) -> None:
        match arg:
            case Measure():
                self.amt = arg.amt
                self.unit = arg.unit
                if locked_in is not None:
                    self.locked_in = locked_in
                else:
                    self.locked_in = arg.locked_in
            case str():
                amount, unit = self.parse_amt(arg)
                self.amt = int(amount * unit.multiplier)
                self.unit = unit
                self.locked_in = bool(locked_in)
            case tuple():
                amount: float = arg[0]
                unit: units.Unit = arg[1]
                self.amt = int(amount * unit.multiplier)
                self.unit = unit
                self.locked_in = bool(locked_in)
            case _:
                raise TypeError(f"'{arg}' of type {type(arg)} doesn't work for the Measure class.")

    @classmethod
    def parse_amt(cls, s: str) -> tuple[Fraction, units.Unit]:
        """Parses a string into a floating-point amount & units.
        
        Used in __init__ so you can do something like `Measure("200 mg")` and it'll work.
        """
        words = s.split()

        amount = Fraction(words.pop(0))
        if words and words[0][0].isnumeric():
            amount += Fraction(words.pop(0))

        unit_name = words.pop(0) if words else ""

        return amount, units.from_name(unit_name)

    def __str__(self) -> str:
        amount = Fraction(self.amt, self.unit.multiplier)

        measured_in_cups = self.unit.category == units.Unit.cups
        plural = measured_in_cups and amount > 1
        unit_str = str(self.unit)
        if plural:
            unit_str += "s"

        if measured_in_cups:
            full_measures = int(amount)
            partial_measures = amount - full_measures
            output = [full_measures, partial_measures]
        else:
            decimal_places = 1 if 0 < amount < 10 else None
            amount = round(float(amount), decimal_places)
            output = [str(amount)]
        return " ".join(str(x) for x in [*output, unit_str] if x)

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __add__(self, other: Measure):

        def should_use_self():
            if self.locked_in and not other.locked_in:
                return True
            elif other.locked_in:
                return False
            else:
                return self.unit.multiplier >= other.unit.multiplier

        assert self.unit.category == other.unit.category

        if should_use_self():
            measure, amt = Measure(self), other.amt
        else:
            measure, amt = Measure(other), self.amt
        measure.amt += amt
        return measure

    def __mul__(self, other: float):
        measure = Measure(self)
        measure.amt = int(round(self.amt * other))
        return measure

    def __floordiv__(self, other: float):
        return self.__mul__(1 / other)

    def __truediv__(self, other: Measure):
        assert self.unit.category == other.unit.category
        return self.amt / other.amt
