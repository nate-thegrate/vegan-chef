import files
from nutrition.nutrition import price_and_nutrition


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
                    parsed_ingreds.append(f"- {section}")
                case dict():
                    name, items = list(section.items())[0]
                    parsed_ingreds.extend([
                        f"\n#### {name}",
                        *(f"- {item}" for item in items),
                        "\n<br>\n" if str_after_this(section) else "",
                    ])
        parsed_ingreds.append("")
        return parsed_ingreds

    @property
    def markdown_text(self):
        if self.calculate_nutrition:
            nutrition = price_and_nutrition(self.ingredients, self.servings)
            filename = files.save_nutrition_html_as_image(self.name)
            markdown_link = f"../../source/nutrition/nutrition_label/images/{filename}"
            nutrition.append(f'<img src="{markdown_link}" alt="{self.name} nutrition facts" width="900" />')
        else:
            nutrition = []
        return "\n".join([
            f"# {self.name}",
            f"*yield: {self.servings} servings*\n" if self.servings > 1 else "",
            "### ingredients",
            *self.parse_ingredients(),
            "<br>\n",
            "### directions:\n",
            *(f"{direction}\n" for direction in self.directions),
            *nutrition,
        ])

    def export_to_recipe_folder(self):
        """Adds the recipe to `recipes/` in markdown format."""
        text = self.markdown_text
        for meal in self.meals:
            with files.recipe(meal, self.name) as recipe_markdown:
                recipe_markdown.write(text)


def main():
    files.yeet_everything()

    recipe_list = [Recipe(*item) for item in files.load_recipes()]

    for recipe in recipe_list:
        recipe.export_to_recipe_folder()


if __name__ == "__main__":
    main()