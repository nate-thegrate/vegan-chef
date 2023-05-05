from typing import Callable
from .measure import Measure
from files import yaml_dicts

daily_values = {name: Measure(amt) for name, amt in yaml_dicts.daily_values()}


def daily_value(name: str, serving_amt: Measure, recipe_amt: Measure = None):
    """returns a %DV based on a single amount, or an HTML table row if 2 amounts are passed."""
    amount_per_day = daily_values[name]
    dv: Callable[[Measure], str] = lambda amount: f"{round((amount / amount_per_day) * 100)}%"
    if recipe_amt is None:
        return dv(serving_amt)
    else:
        return f"<tr><td>{name}<hr></td><td>{dv(serving_amt)}<hr></td><td>{dv(recipe_amt)}<hr></td></tr>"


ingredient_data: dict[str, dict[str, dict[str, dict | str]]] = yaml_dicts.ingredient_data()
ingredient_names = {
    "water": None,
    "fresh fruit (optional)": None,
    "sweetener": "sucralose",
    "nutritional yeast": "fortified premium yeast flakes",
    "oil": "canola oil",
    "sourdough starter": "whole wheat flour",
}


def find_ingredient(ingredient: str):
    words = ingredient.split(" ")
    name_index = 3 if words[1][0].isnumeric() else 2
    name = " ".join(words[name_index:])
    if name in ingredient_names:
        name = ingredient_names[name]
    elif name not in ingredient_data:
        raise KeyError(f"'{name}' (parsed from '{ingredient}') not found in ingredient_data.yaml")
    return name


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


def generate_nutrition_price_data(ingredients: list[str | dict], recipe_servings: float):
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
    nutrition_context = {
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

        nutrition_context.update({
            f"serving_{html_code}_g": grams(amt_per_serving),
            f"serving_{html_code}_dv": dv(amt_per_serving),
            f"recipe_{html_code}_g": grams(total_amt),
            f"recipe_{html_code}_dv": dv(total_amt),
        })

    return nutrition_context, price
