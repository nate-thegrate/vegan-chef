import files
from nutrition import generate_nutrition_price_data


class Recipe():

    def __init__(self, name: str, recipe: dict):
        self.name = name
        self.meals = str(recipe["meal"]).split(", ")
        self.calculate_nutrition: bool = recipe.get("calculate nutrition & price", True)
        self.servings: float = recipe.get("servings", 1.0)
        self.ingredients: list = recipe["ingredients"]
        self.directions = (f"{direction}\n" for direction in recipe["directions"])

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
        return parsed_ingreds

    @property
    def markdown_text(self):
        if self.calculate_nutrition:
            if self.servings == 1:
                raise ValueError(f"U gotta increase number of servings for {self.name}")
            context, price = generate_nutrition_price_data(self.ingredients, self.servings)
            files.nutrition_facts.export(self.name, context)
            nutrition_label_path = f"compile_recipes/nutrition/nutrition_labels/{self.name}/nutrition_facts"
            # relative_image_path = f"../../{nutrition_label_path}.png"
            rendered_html_link = ("https://htmlpreview.github.io/?"
                                  "https://github.com/nate-thegrate/vegan-chef/blob/main/{}.html".format(nutrition_label_path.replace(" ", "%20")))
            price_nutrition_facts = [
                "\n<br>\n",
                f"### calculated ingredient cost:\n",
                f"${price:.2f} for the whole recipe, ${price / self.servings:.2f} per serving",
                "\n<br>\n",
                # f"[![{self.name} nutrition facts]({relative_image_path})]({rendered_html_link})",
                f"[click here for Nutrition Facts]({rendered_html_link})",
            ]
        else:
            price_nutrition_facts = []
        return "\n".join([
            f"# {self.name}",
            f"*yield: {self.servings} servings*\n" if self.servings > 1 else "",
            "### ingredients",
            *self.parse_ingredients(),
            "\n<br>\n",
            "### directions:\n",
            *self.directions,
            *price_nutrition_facts,
        ])

    def export_to_recipe_folder(self):
        """Adds the recipe to `recipes/` in markdown format."""
        text = self.markdown_text
        for meal in self.meals:
            with files.open_recipe(meal, self.name) as recipe_markdown:
                recipe_markdown.write(text)


if __name__ == "__main__":
    files.yeet_everything()

    recipe_list = [Recipe(*item) for item in files.yaml_dicts.recipes()]

    for open_recipe in recipe_list:
        open_recipe.export_to_recipe_folder()
