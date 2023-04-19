from .main import source, UTF8
from .nutrition_facts import nutrition_folder
import yaml


def _load(path) -> dict[str]:
    with open(path, **UTF8) as file:
        return yaml.safe_load(file)


def daily_values():
    daily_values = nutrition_folder.joinpath("daily_values.yaml")
    return _load(daily_values).items()


def ingredient_data():
    ingredient_data = nutrition_folder.joinpath("ingredient_data.yaml")
    return _load(ingredient_data)


def branch_multiplier() -> float:
    """(not currently in use since we aren't multiplying recipes)"""
    branch_config = source.joinpath("branch_config.yaml")
    return _load(branch_config)["recipe_multiplier"]


def recipes():
    recipes = source.joinpath("recipes.yaml")
    return _load(recipes).items()