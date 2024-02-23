document.addEventListener('DOMContentLoaded', function () {
    const buttons = [
        'main dish',
        'side dish',
        'soup',
        'breakfast',
        'bread',
        'drink',
        'dessert',
    ];

    const buttonDiv = document.getElementById('buttons');

    buttons.forEach(label => {
        const button = document.createElement('button');
        button.textContent = label;
        button.className = label.replace(' ', '-');
        button.addEventListener('click', function () { filterRecipes(this) });
        buttonDiv.appendChild(button);
    });
});

var filter = '';

function filterRecipes(button) {
    const category = button.classList[0];
    const showAll = category == filter;
    filter = showAll ? '' : category;

    const recipeLinks = document.querySelectorAll('#recipe-list a');

    recipeLinks.forEach(function (link) {
        var recipeCategory = link.querySelector('.' + category);
        if (!showAll && recipeCategory === null) {
            link.style.display = 'none';
        } else {
            link.style.display = 'block';
            var recipeCategories = link.querySelectorAll(
                '.main-dish, .side-dish, .soup, .breakfast, .bread, .drink, .dessert'
            );
            recipeCategories.forEach(function (category) {
                if (category !== recipeCategory) {
                    category.style.display = 'block';
                } else {
                    category.style.display = showAll ? 'block' : 'none';
                }
            });
        }
    });
}