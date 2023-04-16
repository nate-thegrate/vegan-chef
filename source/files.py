"""Functions & values relating to file paths.

Super nice to have, since imports will work regardless of your working directory.
"""
from pathlib import Path
from shutil import rmtree
import os
import yaml
import jinja2 as jinja
from subprocess import run

script = Path(__file__)
source = Path(script.parent).resolve()
repo = Path(source.parent).resolve()
nutrition = source.joinpath("nutrition")
recipe_export = repo.joinpath("recipes")

_daily_values = nutrition.joinpath("daily_values.yaml")
_ingredient_data = nutrition.joinpath("ingredient_data.yaml")
_branch_config = source.joinpath("branch_config.yaml")
_recipes = source.joinpath("recipes.yaml")


def get_yaml_dict(path) -> dict:
    with open(path, encoding="utf8") as file:
        return yaml.safe_load(file)


def load_daily_values():
    return get_yaml_dict(_daily_values).items()


def load_ingredient_data():
    return get_yaml_dict(_ingredient_data)


def get_branch_multiplier():
    """(not currently in use since we aren't multiplying recipes)"""
    return get_yaml_dict(_branch_config)["recipe_multiplier"]


def load_recipes():
    return get_yaml_dict(_recipes).items()


def yeet_everything():
    """deletes every folder in the `recipes/` directory."""
    for file in os.listdir(recipe_export):
        path = recipe_export.joinpath(file)
        if path.is_dir():
            rmtree(path)


def recipe(meal: str, name: str):
    recipe_path = recipe_export.joinpath(meal)
    if not recipe_path.is_dir():
        recipe_path.mkdir()
    return open(recipe_path.joinpath(f"{name}.md"), "w", encoding="utf8")


nutrition_label = nutrition.joinpath("nutrition_label")
nutrition_images = nutrition_label.joinpath("images")
nutrition_html = nutrition_label.joinpath("nutrition_label_template.html")
nutrition_css = nutrition_label.joinpath("nutrition_label.css")
nutrition_generated_file = nutrition_label.joinpath("generated_nutrition_label.html")


def send_nutrition_to_html(context: dict):
    loader = jinja.FileSystemLoader(str(nutrition_label))
    template = jinja.Environment(loader=loader).get_template("nutrition_label_template.html")

    with open(nutrition_generated_file, "w") as file:
        file.write(template.render(context))


def save_nutrition_html_as_image(recipe_name: str):
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    filename = f"{recipe_name}.png"
    img_path = nutrition_images.joinpath(filename)

    command = [str(x) for x in (firefox_path, '--headless', '--screenshot', img_path, nutrition_generated_file)]
    run(command)
    return filename