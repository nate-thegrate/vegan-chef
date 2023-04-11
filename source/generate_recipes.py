import files
from nutrition.nutrition_facts import price_and_nutrition


class Recipe():

    def __init__(self, name: str, recipe: dict):
        self.name = name
        self.meals = str(recipe["meal"]).split(", ")
        self.calculate_nutrition: bool = recipe.get("calculate nutrition & price", True)
        self.servings: float = recipe.get("servings", 1.0)
        self.ingredients: list = recipe["ingredients"]
        self.directions: list[str] = recipe["directions"]

    def parse_ingredients(self):
        ingreds = self.ingredients
        parsed_ingreds: list[str] = []

        def str_after_this(section) -> bool:
            """Returns `True` if the section after this one is a string
            (i.e. a single ingredient)."""
            next = ingreds.index(section) + 1
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
            f"\n*yield: {self.servings} servings*\n" if self.servings > 1 else "",
            "\n### ingredients\n",
            *self.parse_ingredients(),
            "\n<br>\n",
            "\n### directions:\n",
            *(f"\n{direction}\n" for direction in self.directions),
            price_and_nutrition(self.ingredients, self.servings) if self.calculate_nutrition else "",
        ])

    def export_to_recipe_folder(self):
        """Adds the recipe to `recipes/` in markdown format."""
        for meal in self.meals:
            with files.recipe(meal, self.name) as recipe_markdown:
                recipe_markdown.write(self.markdown_text)


def main():
    files.yeet_everything()

    recipe_list = [Recipe(*item) for item in files.load_recipes()]

    for recipe in recipe_list:
        recipe.export_to_recipe_folder()


if __name__ == "__main__":
    main()