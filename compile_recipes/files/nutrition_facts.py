from .main import compile_recipes
import jinja2 as jinja

nutrition_folder = compile_recipes.joinpath("nutrition")


def html_code(context):
    env = jinja.Environment(loader=jinja.FileSystemLoader(nutrition_folder))
    return env.get_template("nutrition_label_template.html").render(context)


def folder_path(name):
    recipe_name_path = nutrition_folder.joinpath(name)
    if not recipe_name_path.is_dir():
        recipe_name_path.mkdir()
    return recipe_name_path
