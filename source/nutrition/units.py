"""mostly used for the `Unit` type and the `from_name()` function."""


class Unit:
    cups = "cups"
    metric = "metric"
    calories = "Calories"

    def __init__(
        self,
        name: str,
        other_names: set[str],
        category: str = cups,
        multiplier: int = 1,
    ):
        self.name = name
        self.other_names = other_names
        self.category = category
        self.multiplier = multiplier

    def __str__(self) -> str:
        return self.name

    def match(self, name: str) -> bool:
        return self.name == name or name in self.other_names


cup = Unit(
    name="cup",
    other_names={"c"},
    multiplier=8 * 3 * 16,
)
tablespoon = Unit(
    name="tablespoon",
    other_names={"T", "tbsp"},
    multiplier=8 * 3,
)
teaspoon = Unit(
    name="teaspoon",
    other_names={"t", "tsp"},
    multiplier=8,
)
g = Unit(
    name="g",
    other_names={"gram"},
    category=Unit.metric,
    multiplier=1000 * 1000,
)
mg = Unit(
    name="mg",
    other_names={"milligram"},
    category=Unit.metric,
    multiplier=1000,
)
µg = Unit(
    name="µg",
    other_names={"mcg", "microgram"},
    category=Unit.metric,
)
calories = Unit(
    name="",
    other_names={"Cal", "Calories"},
    category=Unit.calories,
)


def from_name(name: str) -> Unit:
    for unit in [cup, tablespoon, teaspoon, g, mg, µg, calories]:
        if unit.match(name):
            return unit
    raise ValueError(f"the name '{name}' doesn't match anything")