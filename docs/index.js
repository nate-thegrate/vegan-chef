function alternateColors(link, index) {
    let classes = link.querySelector('div').classList;
    index % 2 === 1 ? classes.add('even') : classes.remove('even');
}

const buttonNames = [
    'main dish',
    'side dish',
    'soup',
    'breakfast',
    'bread',
    'drink',
    'dessert',
];
const buttonClasses = '.main-dish, .side-dish, .soup, .breakfast, .bread, .drink, .dessert';

document.addEventListener('DOMContentLoaded', function () {
    let buttons = document.getElementById('buttons');
    buttonNames.forEach(label => {
        const button = document.createElement('button');
        button.textContent = label;
        button.className = label.replace(' ', '-');
        button.addEventListener('click', function () { filterRecipes(this) });
        buttons.appendChild(button);
    });
    document.querySelectorAll('#recipe-list a').forEach(alternateColors);
});

var filter = '';

function filterRecipes(button) {
    const category = button.classList[0];
    const showAll = category == filter;
    filter = showAll ? '' : category;

    document.querySelectorAll('#buttons button').forEach(button => {
        let classes = button.classList;
        classes[0] == filter ? classes.add('active') : classes.remove('active');
    });

    let visibleLinks = [];

    document.querySelectorAll('#recipe-list a').forEach(recipeLink => {
        let recipeCategory = recipeLink.querySelector('.' + category);
        function setVisibility(element, comparator) {
            let displayBlock = showAll || recipeCategory !== comparator;
            element.style.display = displayBlock ? 'block' : 'none';
            return displayBlock;
        }

        if (setVisibility(recipeLink, null)) {
            recipeLink.querySelectorAll(buttonClasses).forEach(
                category => setVisibility(category, category)
            );
            visibleLinks.push(recipeLink);
        }
    });
    visibleLinks.forEach(alternateColors);
}