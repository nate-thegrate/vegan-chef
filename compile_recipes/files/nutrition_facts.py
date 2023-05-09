from .main import compile_recipes, UTF8
import jinja2 as jinja
from subprocess import run

nutrition_folder = compile_recipes.joinpath("nutrition")
labels_folder = nutrition_folder.joinpath("nutrition_labels")


def html_code(context):
    env = jinja.Environment(loader=jinja.FileSystemLoader(labels_folder))
    return env.get_template("nutrition_label_template.html").render(context)


def folder_path(name):
    recipe_name_path = labels_folder.joinpath(name)
    if not recipe_name_path.is_dir():
        recipe_name_path.mkdir()
    return recipe_name_path


def export(recipe_name: str, context: dict):
    nutrition_folder_path = folder_path(recipe_name)
    nutrition_html_code = html_code(context)
    nutrition_html_path = nutrition_folder_path.joinpath("nutrition_facts.html")

    if nutrition_html_path.is_file():
        with open(nutrition_html_path, **UTF8) as file:
            if file.read() == nutrition_html_code:
                return

    with open(nutrition_html_path, "w", **UTF8) as file:
        file.write(nutrition_html_code)

    firefox_path = R"C:\Program Files\Mozilla Firefox\firefox.exe"
    img_path = nutrition_folder_path.joinpath("nutrition_facts.png")

    command = [str(x) for x in (firefox_path, '--headless', '--screenshot', img_path, nutrition_html_path)]
    run(command)
