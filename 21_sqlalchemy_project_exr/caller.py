from typing import List

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers import session_decorator
from models import Recipe, Chef
from seeds import recipes

engine = create_engine(config("MY_CONNECTION_STRING"))
Session = sessionmaker(bind=engine)

session = Session()


# 2. Create Recipe
@session_decorator(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    new_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )

    session.add(new_recipe)


# for name, ingredients, instructions in recipes:
#     create_recipe(name, ingredients, instructions)


@session_decorator(session)
# 3. Update Recipe
def update_recipe_by_name(name: str, new_name: str, new_ingredients: str, new_instructions: str) -> None:
    # bulk_update
    records_changed: int = (
        session.query(Recipe)
        .filter_by(name=name)
        .update({
            Recipe.name: new_name,
            Recipe.ingredients: new_ingredients,
            Recipe.instructions: new_instructions
        })
    )

    # standard way
    # recipe_to_update = session.query(Recipe).filter_by(name=name).first()
    #
    # recipe_to_update.name = new_name
    # recipe_to_update.ingredients = new_ingredients
    # recipe_to_update.instructions = new_instructions
    #
    # session.commit()

    return records_changed


# update_recipe_by_name(
#     "Spaghetti Carbonara",
#     "Carbonara Spaghetti",
# "200g spaghetti, 100g pancetta, 2 large eggs, 50g Pecorino cheese, 50g Parmesan cheese, Freshly ground black pepper, Salt, 2 cloves garlic, 1 tbsp olive oil",
# "1. Cook spaghetti in a large pot of boiling salted water until al dente. 2. Meanwhile, heat olive oil in a large skillet over medium heat. Add pancetta and garlic, cooking until the pancetta is crisp. Remove garlic and discard. 3. In a bowl, beat eggs and mix in both cheeses. 4. Drain spaghetti and add to the skillet with pancetta. Remove from heat and quickly mix in the egg and cheese mixture. 5. Season with pepper and serve immediately."
# )


# 4. Delete Recipe
@session_decorator(session)
def delete_recipe_by_name(name: str):
    recipe_to_delete = session.query(Recipe).filter_by(name=name)
    recipe_to_delete.delete()

    return recipe_to_delete


# delete_recipe_by_name('Guacamole')


# 5. Filter Recipes
@session_decorator(session, autoclose_session=False)
def get_recipes_by_ingredient(ingredient_name: str) -> List:
    recipes = (session.query(Recipe)
              .filter(Recipe.ingredients.ilike(f'%{ingredient_name}%'))
              .all())

    return recipes


# all_recipes = get_recipes_by_ingredient('Salt')
# for r in all_recipes:
#     print(r.name)
#
# session.close()


# 6. Recipe Ingredients Swap Transaction
@session_decorator(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name:str) -> None:
    first_recipe = (
        (session.query(Recipe)
        .filter_by(name=first_recipe_name))
        .with_for_update()
        .one()
    )

    second_recipe = (
        (session.query(Recipe)
        .filter_by(name=second_recipe_name))
        .with_for_update()
        .one()
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


# swap_recipe_ingredients_by_name("Chicken Curry", "Carbonara Spaghetti")


# 9. Recipe and Chef Relations
@session_decorator(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()

    if recipe and recipe.chef:
        raise Exception("Recipe: {recipe_name} already has a related chef")

    chef = session.query(Chef).filter_by(name=chef_name).first()

    recipe.chef = chef

    return f"Related recipe {recipe.name} with chef {chef.name}"


# # Create a recipe instance for Bulgarian Musaka
# musaka_recipe = Recipe(
#     name="Musaka",
#     ingredients="Potatoes, Ground Meat, Onions, Eggs, Milk, Cheese, Spices",
#     instructions="Layer potatoes and meat mixture, pour egg and milk mixture on top, bake until golden brown."
# )
#
# # Create a Bulgarian chef instances
# bulgarian_chef1 = Chef(name="Ivan Zvezdev")
# bulgarian_chef2 = Chef(name="Uti Buchvarov")
#
# # Add the recipe instance to the session
# session.add(musaka_recipe)
#
# # Add the chef instances to the session
# session.add(bulgarian_chef1)
# session.add(bulgarian_chef2)
#
# # Commit the changes to the database
# session.commit()

# Test Code 1
# print(relate_recipe_with_chef_by_name("Chicken Carbonara Spaghetti", "Ivan Zvezdev"))

# Test Code 2
# print(relate_recipe_with_chef_by_name("Carbonara Spaghetti", "Chef Uti"))


# 10. Chef and Recipe Integration
@session_decorator(session)
def get_recipes_with_chef() -> str:
    recipes_with_chefs = (
        session.query(Recipe.name, Chef.name)
        .join(Chef, Recipe.chef)
        .all()
    )

    return '\n'.join(
        f"Recipe: {recipe_name} made by chef: {chef_name}"
        for recipe_name, chef_name in recipes_with_chefs
    )


# Create chef instances
chef1 = Chef(name="Gordon Ramsay")
chef2 = Chef(name="Julia Child")
chef3 = Chef(name="Jamie Oliver")
chef4 = Chef(name="Nigella Lawson")

# Create recipe instances associated with chefs
recipe1 = Recipe(name="Beef Wellington", ingredients="Beef fillet, Puff pastry, Mushrooms, Foie gras", instructions="Prepare the fillet and encase it in puff pastry.")
recipe1.chef = chef1

recipe2 = Recipe(name="Boeuf Bourguignon", ingredients="Beef, Red wine, Onions, Carrots", instructions="Slow-cook the beef with red wine and vegetables.")
recipe2.chef = chef2

recipe3 = Recipe(name="Spaghetti Carbonara", ingredients="Spaghetti, Eggs, Pancetta, Cheese", instructions="Cook pasta, mix ingredients.")
recipe3.chef = chef3

recipe4 = Recipe(name="Chocolate Cake", ingredients="Chocolate, Flour, Sugar, Eggs", instructions="Bake a delicious chocolate cake.")
recipe4.chef = chef4

recipe5 = Recipe(name="Chicken Tikka Masala", ingredients="Chicken, Yogurt, Tomatoes, Spices", instructions="Marinate chicken and cook in a creamy tomato sauce.")
recipe5.chef = chef3

session.add_all([chef1, chef2, chef3, chef4, recipe1, recipe2, recipe3, recipe4, recipe5])
session.commit()
print(get_recipes_with_chef())

