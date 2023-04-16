from html2image import Html2Image
import files

hti = Html2Image()
hti.output_path = str(files.nutrition_images)
hti.screenshot(
    html_file=str(files.nutrition_html),
    css_file=str(files.nutrition_css),
    save_as='image.png',
)
