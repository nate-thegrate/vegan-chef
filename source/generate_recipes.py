import os
import yaml
from pathlib import Path
from shutil import rmtree


class Files():
    script = Path(__file__)
    source = Path(script.parent).resolve()
    repo = Path(source.parent).resolve()
    config = source.joinpath("branch_config.yaml")
    recipe_import = source.joinpath("recipes.yaml")
    recipe_export = repo.joinpath("recipes")

    @classmethod
    def recipe(cls, meal: str, name: str):
        recipe_path = cls.recipe_export.joinpath(meal)
        if not recipe_path.is_dir():
            os.makedirs(recipe_path)
        return recipe_path.joinpath(f"{name}.md")


class Recipe():

    def __init__(self, name: str, recipe: dict):
        self.name = name
        self.meals = str(recipe["meal"]).split(", ")
        self.ingredients: list = recipe["ingredients"]
        self.directions: list[str] = recipe["directions"]

    def parse_ingredients(self):
        ingreds = self.ingredients
        parsed_ingreds: list[str] = []

        def str_after_this(item):
            next = ingreds.index(item) + 1
            return next < len(ingreds) and isinstance(ingreds[next], str)

        for section in ingreds:
            match section:
                case str():
                    parsed_ingreds.append(f"- {section}\n")
                case dict():
                    name, items = list(section.items())[0]
                    parsed_ingreds.extend([
                        f"\n#### {name}\n",
                        *(f"- {item}\n" for item in items),
                        "\n<br>\n\n" if str_after_this(section) else "\n",
                    ])
        return parsed_ingreds

    @property
    def markdown_text(self):
        return "".join([
            f"# {self.name}\n",
            "\n### ingredients\n",
            *self.parse_ingredients(),
            "\n<br>\n",
            "\n### directions:\n",
            *(f"\n{direction}\n" for direction in self.directions),
        ])

    def export_to_recipe_folder(self):
        for meal in self.meals:
            with open(Files.recipe(meal, self.name), "w") as recipe_markdown:
                recipe_markdown.write(self.markdown_text)


def yeet_everything():
    """deletes every folder in the `recipes/` directory."""
    for file in os.listdir(Files.recipe_export):
        path = Files.recipe_export.joinpath(file)
        if path.is_dir():
            rmtree(path)


def load_recipes() -> list[Recipe]:
    """Imports data from `recipes.yaml` into a list of `Recipe` objects."""
    with open(Files.recipe_import) as recipe_file:
        recipe_data = dict(yaml.safe_load(recipe_file)).items()
        return [Recipe(*item) for item in recipe_data]


def get_multiplier() -> float:
    """This function isn't currently in use since we aren't multiplying recipes."""
    with open(Files.config) as f:
        return yaml.safe_load(f)["recipe_multiplier"]


def main():
    yeet_everything()

    recipes = load_recipes()

    for recipe in recipes:
        recipe.export_to_recipe_folder()


if __name__ == "__main__":
    main()