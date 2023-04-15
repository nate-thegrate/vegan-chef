# pancakes

*yield: 2 servings*

### ingredients
- 1 c water
- 1/2 t salt
- 1 T erythritol
- 2 T oil
- 1/4 c sourdough starter
- 1 c whole wheat flour
- 2 t baking powder
- 1/8 t guar gum

<br>

### directions:

Mix everything in a bowl, and heat a griddle or pan to 375°F.

Hopefully you know how to flip pancakes.

<br>

### calculated ingredient cost:

$0.59 for the whole recipe, $0.30 per serving

<br>

### nutrition facts

```
                      amount in recipe    amount per serving
Calories                   751     38%           376     19%
Total Fat              31.75 g     41%       15.88 g     20%
Saturated Fat           2.62 g     13%        1.31 g      7%
Cholesterol               0 mg      0%          0 mg      0%
Sodium                 2126 mg     92%       1063 mg     46%
Total Carbs           119.88 g     44%       59.94 g     22%
Fiber                  16.62 g     59%        8.31 g     30%
Sugar                   0.62 g      1%        0.31 g      1%
Sugar Alcohol             12 g     67%           6 g     33%
Protein                   20 g     40%          10 g     20%


Vitamins & Minerals:

Iodine                  134 µg     89%         67 µg     45%
Calcium               58.75 mg      5%      29.38 mg      2%
Iron                   6.47 mg     36%       3.24 mg     18%
Magnesium             212.5 mg     51%     106.25 mg     25%
Phosphorus              550 mg     44%        275 mg     22%
Potassium             587.5 mg     12%     293.75 mg      6%
Copper                  706 µg     78%        353 µg     39%
Manganese              5.56 mg    242%       2.78 mg    121%
Selenium                 38 µg     69%         19 µg     35%
Molybdenum               91 µg    202%         46 µg    102%
Thiamin                 788 µg     66%        394 µg     33%
Riboflavin              200 µg     15%        100 µg      8%
Niacin                 9.38 mg     59%       4.69 mg     29%
Vitamin B6              419 µg     25%        210 µg     12%
Folic Acid               60 µg     15%         30 µg      8%
Zinc                      5 mg     45%        2.5 mg     23%
```

test:
```math
SE = \frac{\sigma}{\sqrt{n}}
```


```math
\documentclass[border=2]{standalone}
\usepackage{xparse}
\usepackage{booktabs}
\newlength{\NFwidth}
\setlength{\NFwidth}{2.5in}

\NewDocumentCommand{\NFelement}{mmm}{\large\textbf{#1} #2\hfill #3}
\NewDocumentCommand{\NFline}{O{l}m}{\makebox[\NFwidth][#1]{#2}}
\NewDocumentCommand{\NFentry}{sm}{%
  \makebox[.5\NFwidth][l]{\large
    \IfBooleanT{#1}{\makebox[0pt][r]{\textbullet\ }}%
    #2}\ignorespaces}
\NewDocumentCommand{\NFtext}{+m}
 {\parbox{\NFwidth}{\raggedright#1}}

\newcommand{\NFtitle}{\multicolumn{1}{c}{\Huge\bfseries Nutrition Facts}}

\newcommand{\NFRULE}{\midrule[6pt]}
\newcommand{\NFRule}{\midrule[3pt]}
\newcommand{\NFrule}{\midrule}

\begin{document}
\sffamily
\fbox{%
\begin{tabular}{@{}p{\NFwidth}@{}}
\NFtitle\\
\NFtext{Serving Size 2 tbsp.\ (33\,g)}\\
\NFtext{Servings Per Container 7}\\
\NFRULE
\NFline{Amount Per Serving}\\
\NFrule
\NFelement{Calories}{20}{Calories from Fat 10}\\
\NFRule
\NFline[r]{\% Daily Value*}\\
\NFrule
\NFelement{Total Fat}{1\,g}{2\%}\\
\NFrule
\NFelement{Sodium}{190\,mg}{8\%}\\
\NFrule
\NFelement{Total Carbohydrate}{2\,g}{1\%}\\
\NFrule
\NFelement{Protein}{1\,g}{}\\
\NFRule
\NFentry{Vitamin A 2\%}
\NFentry*{Vitamin C 15\%}\\
\NFentry{Iron 10\%}
\NFentry*{Vitamin B6 20\%}\\
\NFentry{Vitamin B12 4\%}\\
\NFrule
\NFtext{Not a significant source of saturated fat,
  trans fat, cholesterol, dietary fiber, sugars,
  and calcium.}\\
\NFrule
\NFtext{* Percent Daily Values are based on a
  2,000 calorie diet.}
\end{tabular}}
\end{document}
```
