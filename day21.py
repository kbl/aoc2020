import ioaoc
import collections

test_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def parse(lines):
    parsed_lines = []
    for line in lines:
        ingredients, allergens = line.split("(contains ")

        ingredients = [ingredient for ingredient in ingredients.split(" ") if ingredient]
        allergens = allergens[:-1].split(", ")

        parsed_lines.append((ingredients, allergens))
    return parsed_lines


def simplify(all_lines, known_allergens):
    changed = False
    for allergen, ingredient in known_allergens.items():
        for ingredients, allergens in all_lines:
            if ingredient in ingredients:
                changed = True
                ingredients.remove(ingredient)
            if allergen in allergens:
                changed = True
                allergens.remove(allergen)
    return changed


def map_ingredients_to_allergens(all_lines):
    all_ingredients = {}

    for ingredients, allergens in all_lines:
        for allergen in allergens:
            ingredients_set = set(ingredients)
            if allergen not in all_ingredients:
                all_ingredients[allergen] = ingredients_set
                continue
            
            current_ingredients = all_ingredients[allergen]
            intersection = current_ingredients.intersection(ingredients_set)
            if intersection:
                all_ingredients[allergen] = intersection
                continue

            all_ingredients[allergen] = current_ingredients.union(ingredients_set)

    return all_ingredients


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day21_input.txt")

    parsed_lines = parse(lines)

    changed = True
    known_allergens = {}

    while changed:
        all_allergens = map_ingredients_to_allergens(parsed_lines)

        for allergen, ingredients in all_allergens.items():
            if len(ingredients) == 1:
                [ingredient] = ingredients
                known_allergens[allergen] = ingredient

        changed = simplify(parsed_lines, known_allergens)

    print(">", sum((len(ingredients) for (ingredients, _) in parsed_lines)))
    print(">>", ",".join([ingredient for _, ingredient in sorted(known_allergens.items())]))
