from __future__ import annotations
from fractions import Fraction
from nutrition import units
import files


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
            amount = round(float(amount), 2)
            if amount.is_integer():
                amount = int(amount)
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
def daily_value(name, amount):
    amount_per_day = daily_values[name]
    return f"{round((amount / amount_per_day) * 100)}%"

ingredient_data = files.load_ingredient_data()
ingredient_names = {
    "water": None,
    "oil": "canola oil",
    "sourdough starter": "whole wheat flour",
}
remap_ingredient_name = lambda name: ingredient_names.get(name, name)


def price_and_nutrition(ingredients: list[str | dict], recipe_servings: float):

    def serving_info(main_info, info_per_serving):
        if recipe_servings > 1:
            return f"{main_info} {info_per_serving}"
        else:
            return str(main_info)

    def unpack() -> list[str]:
        new_ingredients = []
        for ingredient in ingredients:
            match ingredient:
                case str():
                    new_ingredients.append(ingredient)
                case dict():
                    for stuff in ingredient:
                        new_ingredients.append(stuff)
        return new_ingredients

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

    ingred_list: list[str] = unpack()
    for ingredient in ingred_list:
        name = ingredient.split(" ")
        name_index = 3 if name[2][0].isnumeric() else 2
        name = " ".join(name[name_index:])
        if name not in ingredient_data and name not in ingredient_names:
            raise KeyError(f"'{name}' (parsed from '{ingredient}') not found in ingredient_data.yaml")
        name = remap_ingredient_name(name)
        if name is None:
            continue

        data = ingredient_data[name]

        ingredient_measure = Measure(ingredient)
        serving_measure = Measure(data["serving size"])
        servings = ingredient_measure / serving_measure
        price += data["container price"] / data["servings per container"] * servings
        nutrition_facts: dict[str, str | dict] = data["nutrition facts"]
        for nutrient, amount in nutrition_facts.items():
            if nutrient == "Vitamins":
                for vitamin, amt in amount.items():
                    measure = Measure(amt) * servings
                    if vitamin in vitamin_facts:
                        vitamin_facts[vitamin] += measure
                    else:
                        vitamin_facts[vitamin] = measure
                continue

            overall_nutrition_facts[nutrient] += (Measure(amount) * servings)

    amount_table_header = " " * 22 + "amount in recipe    amount per serving"

    return "\n".join([
        "\n<br>\n",
        f"### calculated ingredient cost:\n",
        serving_info(f"${price:.2f}", f"for the whole recipe, ${price / recipe_servings:.2f} per serving"),
        "\n<br>\n",
        "### nutrition facts\n",
        "```",
        amount_table_header,
        *(f"{name:20} {amt:>9} {daily_value(name, amt):>7} {amt//recipe_servings:>13} {daily_value(name, amt//recipe_servings):>7}" for name, amt in overall_nutrition_facts.items()),
        "\n\nVitamins & Minerals:\n",
        *(f"{name:20} {amt:>9} {daily_value(name, amt):>7} {amt//recipe_servings:>13} {daily_value(name, amt//recipe_servings):>7}" for name, amt in vitamin_facts.items()),
        "```",
    ])
    # return f"Nutrition Facts\n\n{overall_nutrition_facts}\n\n" f"Vitamins & Minerals\n\n{vitamin_facts}"

    # net_carbs = None
    # if "Total Carbs" in ingredients:
    #     estimated_starch = total_carbs - fiber - sugar - sugar_alcohol
    #     if made_with_resistant_starch:
    #         # current evidence suggests that resistant starch still has an impact on blood sugar,
    #         # about 50% as strong as regular starch
    #         estimated_starch /= 2
    #         fiber -= estimated_starch  # might as well adjust fiber accordingly
    #     net_carbs = sugar + estimated_starch