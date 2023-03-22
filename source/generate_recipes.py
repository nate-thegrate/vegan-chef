import os
import yaml
from shutil import rmtree

with open("branch_config.yaml") as f:
    multiplier = yaml.safe_load(f)["recipe_multiplier"]

recipe_filepath = '../recipes'


class Recipe():

    def __init__(self, name: str, recipe: dict[str, str | list[str]]):
        self.name = name
        self.meals: list[str] = recipe["meal"].split(", ")
        self.ingredients: list = recipe["ingredients"]
        self.directions: list[str] = recipe["directions"]
    
    @property
    def filepaths(self):
        paths = []
        for name in self.meals:
            filepath = os.path.join(recipe_filepath, name)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            paths.append(filepath)
        return (os.path.join(path, f"{self.name}.md") for path in paths)
    
    @property
    def ingredients_markdown(self):
        ingreds = self.ingredients
        parsed_ingreds = []
        
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
            *self.ingredients_markdown,
            "\n<br>\n",
            "\n### directions:\n",
            *(f"\n{direction}\n" for direction in self.directions),
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
            for filepath in r.filepaths:
                with open(filepath, "w") as recipe_markdown:
                    recipe_markdown.write(r.markdown_text)
    else:
        pass  # Coming soon!
        # TODO: make `Ingredient` class with fancy parsing and multiplication


if __name__ == "__main__":
    main()