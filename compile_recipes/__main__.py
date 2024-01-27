import files
from nutrition import generate_nutrition_price_data
import jinja2 as jinja


def dashed(name: str):
    return name.replace(" ", "-")


class Recipe:
    def __init__(self, name: str, recipe: dict):
        self.name = name
        self.filename = f"{dashed(name)}.html"
        self.meals = str(recipe["meal"]).split(", ")
        self.calculate_nutrition: bool = recipe.get("calculate nutrition & price", True)
        self.servings: float = recipe.get("servings", 1.0)
        self.ingredients: list = recipe["ingredients"]
        self.directions = (f"<p>{direction}</p>\n" for direction in recipe["directions"])

    def parse_ingredients(self):
        ingreds = self.ingredients
        parsed_ingreds: list[str] = []

        def str_after_this(section) -> bool:
            """Returns `True` if the section after this one is a string
            (i.e. a single ingredient)."""
            next = ingreds.index(section) + 1
            return next < len(ingreds) and isinstance(ingreds[next], str)

        for i, section in enumerate(ingreds):
            match section:
                case str():
                    parsed_ingreds.append(
                        f'<input type="checkbox" id="ingredient{i}">\n'
                        f'<label for="ingredient{i}">{section}</label><br>\n'
                    )
                case dict():
                    name, items = list(section.items())[0]
                    parsed_ingreds.extend(
                        [
                            f"\n<h3>{name}</h3>",
                            *(f"- {item}" for item in items),
                            "\n<br>\n" if str_after_this(section) else "",
                        ]
                    )
        return parsed_ingreds

    @property
    def hyperlink(self):
        meal_tags = " ".join(f'<div class="{dashed(meal)}">{meal}</div>' for meal in self.meals)
        return f'<a href="{self.filename}"><div><div class="name">{self.name}</div> {meal_tags}</div></a>'

    @property
    def html_text(self):
        if self.calculate_nutrition:
            if self.servings == 1:
                raise ValueError(f"U gotta increase number of servings for {self.name}")
            context, price = generate_nutrition_price_data(self.ingredients, self.servings)
            price_nutrition_facts = [
                "\n<br>\n",
                f"<h2>calculated ingredient cost</h2>\n",
                f"<p>${price:.2f} for the whole recipe, ${price / self.servings:.2f} per serving</p>",
                "\n<br>\n",
                "</section>",
                files.nutrition_facts.html_code(context),
            ]
        else:
            price_nutrition_facts = ["</section>"]
        return "\n".join(
            [
                "<!DOCTYPE html>",
                '<html lang="en">',
                "",
                "<head>",
                '  <meta charset="UTF-8">',
                '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
                '<link rel="stylesheet" href="recipe.css">',
                "  <title>vegan chef 😎</title>",
                "</head>",
                "<body>",
                '<section id="recipe">',
                f"<h1>{self.name}</h1>",
                f"<p><i>yield: {self.servings} servings</i></p>\n" if self.servings > 1 else "",
                "<h2>ingredients</h2>",
                *self.parse_ingredients(),
                "\n<br>\n",
                "<h2>directions</h2>\n",
                *self.directions,
                *price_nutrition_facts,
                "</body>",
            ]
        )


if __name__ == "__main__":
    files.yeet_everything()

    recipe_list = [Recipe(*item) for item in files.yaml_dicts.recipes()]

    for recipe in recipe_list:
        files.export_recipe(recipe.filename, recipe.html_text)

    for filename in ["recipe.css", "index.css"]:
        files.copy_into_recipes(filename)

    files.generate_index([recipe.hyperlink for recipe in recipe_list])
