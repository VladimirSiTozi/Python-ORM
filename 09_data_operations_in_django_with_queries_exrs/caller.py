import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car


# Create queries within functions


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species
    )

    return f"{pet.name} is a very cute {pet.species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"

# create_artifact('golden cup', 'Indiana Jones', 260, 'sth text', True)


def rename_artifact(artifact: Artifact, new_name: str):
    # optimal for multiple records
    # Artifact.objects.filter(is_magical=True, age__gt=250, pk=artifact.pk).update(name=new_name)

    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

# golden_cup = Artifact.objects.get(pk=1)
# print(golden_cup.name)
# rename_artifact(golden_cup, 'wooden_cup')
# print(golden_cup.name)


def delete_all_artifacts():
    Artifact.objects.all().delete()

# delete_all_artifacts()


# TEST CODE:
# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)


def show_all_locations():
    all_locations = Location.objects.all().order_by('-id')

    return '\n'.join(str(l) for l in all_locations)

# print(show_all_locations())


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()

# new_capital()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')

# print(get_capitals())


def delete_first_location():
    Location.objects.first().delete()

# delete_first_location()


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        str_year = str(car.year)
        discount = sum(int(d) for d in str_year)
        car.price_with_discount = float(car.price) - (float(car.price) * (discount / 100))
        car.save()

# apply_discount()


def get_recent_cars():
    cars_over_2020 = Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')
    return cars_over_2020

# print(get_recent_cars())


def delete_last_car():
    Car.objects.last().delete()