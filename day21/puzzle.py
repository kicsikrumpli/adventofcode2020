from collections import defaultdict
from functools import reduce
from pprint import pprint

if __name__ == '__main__':
    allergen_index = defaultdict(lambda: list())

    ingredient_count = defaultdict(lambda: 0)

    with open('input.txt', 'rt') as puzzle:
        for line in puzzle:
            line = line.strip()
            ingredients, allergens = line.split('(')
            allergens = allergens.replace('contains ', '').replace(')', '').split(', ')
            ingredients = ingredients.strip().split(' ')
            for allergen in allergens:
                allergen_index[allergen].append(set(ingredients))

            for ingredient in ingredients:
                ingredient_count[ingredient] += 1

    for key in allergen_index.keys():
        allergen_index[key] = reduce(lambda a, b: a.intersection(b), allergen_index[key])

    allergen_index = dict(allergen_index)

    while True:
        if all(len(ingredients) == 1 for ingredients in allergen_index.values()):
            break
        else:
            # print('---')
            pass

        for allergen, ingredients in allergen_index.items():
            if len(ingredients) == 1:
                ingredient, *_ = ingredients
                # print(f'removing ingredient {ingredient} for allergen {allergen} from...')
                for other_allergen, other_ingredients in allergen_index.items():
                    if allergen != other_allergen and ingredient in allergen_index[other_allergen]:
                        # print(other_allergen)
                        allergen_index[other_allergen].remove(ingredient)

    allergen_index = {
        allergen: ingredient
        for allergen, ingredients in allergen_index.items()
        for ingredient in ingredients
    }

    print('allergen index: ')
    pprint(allergen_index)

    allergen_ingredients = set(allergen_index.values())

    print('allergenic ingredients: ')
    pprint(allergen_ingredients)

    ingredients_with_no_allergens = [
        count
        for ingredient, count
        in ingredient_count.items()
        if ingredient not in allergen_ingredients
    ]

    print(f'Number of times any of the ingredients appear, that cannot possibly contain any allergens: {sum(ingredients_with_no_allergens)}')

    ingredients_in_order_of_allergens = ",".join(
        ingredient
        for allergen, ingredient
        in sorted(list(allergen_index.items()), key=lambda x: x[0])
    )

    print(f'all the ingredients containing allergens in lexical order of ingredients: {ingredients_in_order_of_allergens}')
