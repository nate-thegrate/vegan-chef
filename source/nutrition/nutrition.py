from __future__ import annotations
from fractions import Fraction
from nutrition import units
import files
from typing import Callable


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


daily_values = {name: Measure(amt) for name, amt in files.load_daily_values()}


def daily_value(name: str, serving_amt: Measure, recipe_amt: Measure = None):
    """returns a %DV based on a single amount, or an HTML table row if 2 amounts are passed."""
    amount_per_day = daily_values[name]
    dv: Callable[[Measure], str] = lambda amount: f"{round((amount / amount_per_day) * 100)}%"
    if recipe_amt is None:
        return dv(serving_amt)
    else:
        return f"<tr><td>{name}<hr></td><td>{dv(serving_amt)}<hr></td><td>{dv(recipe_amt)}<hr></td></tr>"


ingredient_data: dict[str, dict[str, dict[str, dict | str] | any]] = files.load_ingredient_data()
ingredient_names = {
    "water": None,
    "oil": "canola oil",
    "sourdough starter": "whole wheat flour",
}
def find_ingredient(ingredient: str):
    words = ingredient.split(" ")
    name_index = 3 if words[2][0].isnumeric() else 2
    name = " ".join(words[name_index:])
    if name not in ingredient_data and name not in ingredient_names:
        raise KeyError(f"'{name}' (parsed from '{ingredient}') not found in ingredient_data.yaml")
    return ingredient_names.get(name, name)

html_template_names = {
    "Total Fat": "fat",
    "Saturated Fat": "sat_fat",
    "Cholesterol": "cholesterol",
    "Sodium": "sodium",
    "Total Carbs": "carbs",
    "Fiber": "fiber",
    "Sugar": "sugar",
    "Sugar Alcohol": "sugar_alc",
    "Protein": "protein",
}.items()


def price_and_nutrition(ingredients: list[str | dict], recipe_servings: float):
    """Compiles recipe nutrition facts and calls `send_nutrition_to_html()` to create a nutrition label.
    
    Returns the calculated cost of all ingredients (as a list of strings in Markdown format).
    """
    price = 0.0
    overall_nutrition_facts = {
        "Calories": Measure("0"),
        "Total Fat": Measure("0 g"),
        "Saturated Fat": Measure("0 g"),
        "Cholesterol": Measure("0 mg"),
        "Sodium": Measure("0 mg"),
        "Total Carbs": Measure("0 g"),
        "Fiber": Measure("0 g"),
        "Sugar": Measure("0 g"),
        "Sugar Alcohol": Measure("0 g"),
        "Protein": Measure("0 g"),
    }
    vitamin_facts = {}

    parsed_ingreds: list[str] = []
    for ingredient in ingredients:
        match ingredient:
            case str():
                parsed_ingreds.append(ingredient)
            case dict():
                parsed_ingreds.extend(ingredient.values())

    for ingredient in parsed_ingreds:
        name = find_ingredient(ingredient)
        if name is None:
            continue

        data = ingredient_data[name]

        ingredient_servings = Measure(ingredient) / Measure(data["serving size"])
        price += float(data["container price"] / data["servings per container"]) * ingredient_servings
        for nutrient, amount in data["nutrition facts"].items():
            if nutrient == "Vitamins":
                for vitamin, amt in amount.items():
                    measure = Measure(amt) * ingredient_servings
                    if vitamin in vitamin_facts:
                        vitamin_facts[vitamin] += measure
                    else:
                        vitamin_facts[vitamin] = measure
            else:
                overall_nutrition_facts[nutrient] += (Measure(amount) * ingredient_servings)

    vitamins = "\n".join(daily_value(name, amt // recipe_servings, amt) for name, amt in vitamin_facts.items())
    context = {
        "servings": recipe_servings,
        "serving_calories": str(overall_nutrition_facts["Calories"] // recipe_servings),
        "recipe_calories": str(overall_nutrition_facts["Calories"]),
        "vitamins": vitamins,
    }

    for nutrient_name, html_code in html_template_names:
        total_amt = overall_nutrition_facts[nutrient_name]
        amt_per_serving = total_amt // recipe_servings
        dv = lambda amt: daily_value(nutrient_name, amt)
        grams = lambda amt: str(amt).replace(" ", "")

        context.update({
            f"serving_{html_code}_g": grams(amt_per_serving),
            f"serving_{html_code}_dv": dv(amt_per_serving),
            f"recipe_{html_code}_g": grams(total_amt),
            f"recipe_{html_code}_dv": dv(total_amt),
        })

    files.send_nutrition_to_html(context)

    return [
        "\n<br>\n",
        f"### calculated ingredient cost:\n",
        f"${price:.2f} for the whole recipe, ${price / recipe_servings:.2f} per serving",
        "\n<br>\n",
    ]
