from pathlib import Path
from shutil import rmtree

source = Path(__file__).parent.parent.resolve()
repo = source.parent.resolve()

recipe_export = repo.joinpath("recipes")

UTF8 = {"encoding": "utf8"}


def yeet_everything():
    """deletes every folder in the `recipes/` directory."""
    for file in recipe_export.iterdir():
        path = recipe_export.joinpath(file)
        if path.is_dir():
            rmtree(path)


def open_recipe(meal: str, name: str):
    recipe_path = recipe_export.joinpath(meal)
    if not recipe_path.is_dir():
        recipe_path.mkdir()
    return open(recipe_path.joinpath(f"{name}.md"), "w", **UTF8)
