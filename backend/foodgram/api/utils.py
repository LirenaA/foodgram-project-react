def add_ingredients(recipe, ingredients_amounts):
    recipe.ingredients.clear()
    for ingredient_amount in ingredients_amounts:
        ingredient = ingredient_amount['ingredient']['id']
        amount = ingredient_amount['amount']
        recipe.ingredients.add(
            ingredient, through_defaults={'amount': amount}
        )
    return recipe


def create_shopping_list(ingredients, txt_file):
    text = ['Список ингредиентов: \n \n']

    for ingredient in ingredients:
        amount = ingredient['amount']
        text.append(f'{ingredient["name"]}  - {amount} '
                    f' ({ingredient["measurement_unit"]})\n')
    text = ''.join(text)

    with open(txt_file, 'w+') as file:
        file.write(text)
