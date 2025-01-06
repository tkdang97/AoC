from utils.data import *
from collections import deque


def parse(data):
    res = []
    for line in data.splitlines():
        ingredients, allergens = line.split("(")
        ingredients = ingredients.split()
        allergens = allergens.rstrip(")\n").split(", ")
        allergens[0] = allergens[0].split()[1]
        res.append((ingredients, allergens))
    return res


def create_mapping(foods):
    possible = {}
    all_ingredients = set()
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in possible:
                possible[allergen] = set(ingredients)
            else:
                possible[allergen] &= set(ingredients)
        all_ingredients |= set(ingredients)

    check = deque(possible.keys())
    mapping = {}
    while len(check) > 0:
        allergen = check.popleft()
        possibilities = possible[allergen] - set(mapping.values())
        if len(possibilities) == 1:
            mapping[allergen] = possibilities.pop()
        else:
            check.append(allergen)
    return mapping, all_ingredients


def part1(foods):
    mapping, all_ingredients = create_mapping(foods)
    no_allergens = all_ingredients - set(mapping.values())
    return sum(1 for ingredients, _ in foods for ingredient in ingredients if ingredient in no_allergens)


def part2(foods):
    mapping, _ = create_mapping(foods)
    res = []
    for allergen in sorted(mapping.keys()):
        res.append(mapping[allergen])
    return ",".join(res)


test = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

data = get_and_write_data(21, 2020)
foods = parse(data)
print_output(part1(foods), part2(foods))
