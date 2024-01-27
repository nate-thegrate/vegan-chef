from pathlib import Path
from shutil import copy, rmtree
import jinja2 as jinja

compile_recipes = Path(__file__).parent.parent.resolve()
repo = compile_recipes.parent.resolve()

recipe_export = repo.joinpath("recipes")


def generate_index(recipes: list[str]):
    env = jinja.Environment(loader=jinja.FileSystemLoader(repo))
    html = env.get_template("index.html").render(recipe_list="\n    ".join(recipes))

    with open(recipe_export.joinpath("index.html"), "w", encoding="utf8") as index_file:
        index_file.write(html)


def yeet_everything():
    """clears out the `recipes/` directory."""
    rmtree(recipe_export)
    recipe_export.mkdir()


def export_recipe(filename: str, contents: str):
    """Adds the recipe to `recipes/` in html format."""
    with open(recipe_export.joinpath(filename), "w", encoding="utf8") as recipe_html:
        recipe_html.write(contents)


def copy_into_recipes(filename: str):
    copy(filename, f"recipes/{filename}")
