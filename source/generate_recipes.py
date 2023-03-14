import os
import yaml
from shutil import rmtree

with open("branch_config.yaml") as f:
    multiplier = yaml.safe_load(f)["recipe_multiplier"]

recipe_filepath = '../recipes'


class Recipe():

    def __init__(self, name: str, recipe: dict[str, str | list[str]]):
        self.name = name
        self.meal: str = recipe["meal"]
        self.ingredients: list[str] = recipe["ingredients"]
        self.directions: list[str] = recipe["directions"]

    @property
    def filepath(self):
        meal_folder_path = os.path.join(recipe_filepath, self.meal)
        if not os.path.exists(meal_folder_path):
            os.makedirs(meal_folder_path)
        return os.path.join(meal_folder_path, f"{self.name}.md")

    @property
    def markdown_text(self):
        return "".join([
            f"# {self.name}\n",
            "\n### ingredients\n",
            *[f"- {ingredient}\n" for ingredient in self.ingredients],
            "\n<br>\n",
            "\n### directions:\n",
            *[f"\n{direction}\n" for direction in self.directions],
        ])


def yeet_all_recipes():
    for file in os.listdir(recipe_filepath):
        path = os.path.join(recipe_filepath, file)
        if os.path.isdir(path):
            rmtree(path)


def main():
    yeet_all_recipes()

    with open("recipes.yaml") as recipe_yaml:
        recipes = yaml.safe_load(recipe_yaml)

    if multiplier == 1:
        for name in recipes:
            r = Recipe(name, recipes[name])
            with open(r.filepath, "w") as recipe_markdown:
                recipe_markdown.write(r.markdown_text)
    else:
        pass  # Coming soon!
        # TODO: make `Ingredient` class with fancy parsing and multiplication


if __name__ == "__main__":
    main()