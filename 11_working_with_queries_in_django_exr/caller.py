import os
import django
from django.db.models import Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from typing import List
from main_app.choises import OSChoices, MealTypeChoice, DungeonDifficultyChoices, WorkoutTypeChoices
# from populate_db import populate_model_with_data


# Create and check models

# ArtworkGallery
def show_highest_rated_art() -> str:
    top_artist = ArtworkGallery.objects.order_by('-rating', 'id').first()
    # SELECT * FROM artwork ORDER BY rating DESC, id ASC LIMIT 1

    return f"{top_artist.art_name} is the highest-rated art with a {top_artist.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art
    ])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# Laptop
def show_the_most_expensive_laptop() -> str:
    top_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{top_laptop.brand} is the most expensive laptop available for {top_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=('Asus', 'Lenovo')).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=('Apple', 'Dell')).update(memory=16)


def update_operation_systems():
    # Solution 1
    Laptop.objects.update(
        operation_system=Case(
            When(brand='Asus', then=Value(OSChoices.WINDOWS)),
            When(brand='Apple', then=Value(OSChoices.MACOS)),
            When(brand__in=('Dell', 'Acer'), then=Value(OSChoices.LINUX)),
            When(brand='Lenovo', then=Value(OSChoices.CHROME_OS))
        )
    )

    # Solution 2
    # Laptop.objects.filter(brand='Asus').update(operation_system=OSChoices.WINDOWS)
    # Laptop.objects.filter(brand='Apple').update(operation_system=OSChoices.MACOS)
    # Laptop.objects.filter(brand_in=('Dell', 'Acer')).update(operation_system=OSChoices.LINUX)
    # Laptop.objects.filter(brand='Lenovo').update(operation_system=OSChoices.CHROME_OS)


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# ChessPlayer
def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(*args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=[2399, 2300]).update(title='IM')


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=[2299, 2200]).update(title='FM')


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=[2199, 0]).update(title='regular player')


# Meal
def set_new_chefs():
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoice.BREAKFAST, then=Value('Gordon Ramsay')),
            When(meal_type=MealTypeChoice.LUNCH, then=Value('Julia Child')),
            When(meal_type=MealTypeChoice.DINNER, then=Value('Jamie Oliver')),
            When(meal_type=MealTypeChoice.SNACK, then=Value('Thomas Keller'))
        )
    )


def set_new_preparation_times():
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=MealTypeChoice.BREAKFAST, then=Value('10 minutes')),
            When(meal_type=MealTypeChoice.LUNCH, then=Value('12 minutes')),
            When(meal_type=MealTypeChoice.DINNER, then=Value('15 minutes')),
            When(meal_type=MealTypeChoice.SNACK, then=Value('5 minutes'))
        )
    )


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoice.BREAKFAST, MealTypeChoice.DINNER]).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoice.LUNCH, MealTypeChoice.SNACK]).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoice.LUNCH, MealTypeChoice.SNACK]).delete()


# Dungeon
def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(difficulty=DungeonDifficultyChoices.HARD).order_by('-location')
    result = []

    for dungeon in hard_dungeons:
        result.append(f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!")

    return '\n'.join(result)


def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value('The Erased Thombs')),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value('The Lost Haunt')),
        )
    )


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty=DungeonDifficultyChoices.EASY).update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value(25)),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value(75))
        )
    )


def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(reward='1000 Gold')
    Dungeon.objects.filter(location__startswith='E').update(reward='New dungeon unlocked')
    Dungeon.objects.filter(location__endswith='s').update(reward='Dragonheart Amulet')


def set_new_locations():
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss'))
        )
    )


# Workout
def show_workouts():
    all_workout = Workout.objects.filter(
        workout_type__in=[WorkoutTypeChoices.CALISTHENICS,
                          WorkoutTypeChoices.CROSSFIT]
    ).order_by('name', 'workout_type', 'difficulty')
    result = []

    for workout in all_workout:
        result.append(f'{workout.name} from {workout.workout_type} type has {workout.difficulty} difficulty!')

    return '\n'.join(result)


def get_high_difficulty_cardio_workouts():
    hard_workouts = (Workout.objects.filter(workout_type=WorkoutTypeChoices.CARDIO, difficulty='High')
                     .order_by('instructor'))

    return hard_workouts


def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoices.CARDIO, then=Value('John Smith')),
            When(workout_type=WorkoutTypeChoices.STRENGTH, then=Value('Michael Williams')),
            When(workout_type=WorkoutTypeChoices.YOGA, then=Value('Emily Johnson')),
            When(workout_type=WorkoutTypeChoices.CROSSFIT, then=Value('Sarah Davis')),
            When(workout_type=WorkoutTypeChoices.CALISTHENICS, then=Value('Chris Heria'))
        )
    )


def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes'))
        )
    )


def delete_workouts():
    Workout.objects.exclude(
        workout_type__in=[
            WorkoutTypeChoices.STRENGTH,
            WorkoutTypeChoices.CALISTHENICS]
    ).delete()

# Run and print your queries
# populate_model_with_data(Workout,20)


# TEST: ArtworkGallery
# print(show_highest_rated_art())

# art1 = ArtworkGallery(
#     art_name='eho1',
#     artist_name='Pesho',
#     rating=10,
#     price=2000
# )
#
# art2 = ArtworkGallery(
#     art_name='eho2',
#     artist_name='Pesho',
#     rating=18,
#     price=3300
# )
#
# bulk_create_arts(art1, art2)

# delete_negative_rated_arts()


# TEST: Laptop
# print(show_the_most_expensive_laptop())

# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)

# update_to_512_GB_storage()
# update_to_16_GB_memory()
# update_operation_systems()
# delete_inexpensive_laptops()


# TEST: ChessPlayer
# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())


# TEST: Meal
# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()
#
# # Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)


# TEST: Dungeon
# print(show_hard_dungeons())
# Create two instances
# dungeon1 = Dungeon(
#     name="Dungeon 1",
#     boss_name="Boss 1",
#     boss_health=1000,
#     recommended_level=75,
#     reward="Gold",
#     location="Eternal Hell",
#     difficulty="Hard",
# )
#
# dungeon2 = Dungeon(
#     name="Dungeon 2",
#     boss_name="Boss 2",
#     boss_health=400,
#     recommended_level=25,
#     reward="Experience",
#     location="Crystal Caverns",
#     difficulty="Easy",
# )
#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)

# TEST: Workout
# print(show_workouts())
# Create two Workout instances
# workout1 = Workout.objects.create(
#     name="Push-Ups",
#     workout_type="Calisthenics",
#     duration="10 minutes",
#     difficulty="Intermediate",
#     calories_burned=200,
#     instructor="Bob"
# )
#
# workout2 = Workout.objects.create(
#     name="Running",
#     workout_type="Cardio",
#     duration="30 minutes",
#     difficulty="High",
#     calories_burned=400,
#     instructor="Lilly"
# )
#
# # Run the functions
# print(show_workouts())
#
# high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
# for workout in high_difficulty_cardio_workouts:
#     print(f"{workout.name} by {workout.instructor}")
#
# set_new_instructors()
# for workout in Workout.objects.all():
#     print(f"Instructor: {workout.instructor}")
#
# set_new_duration_times()
# for workout in Workout.objects.all():
#     print(f"Duration: {workout.duration}")
