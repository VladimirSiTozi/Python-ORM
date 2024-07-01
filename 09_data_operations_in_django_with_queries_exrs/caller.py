import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


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


def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return "\n".join(str(t) for t in unfinished_tasks)

# print(show_unfinished_tasks())


def complete_odd_tasks() -> None:
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str):
    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
    Task.objects.filter(title=task_title).update(description=decoded_text)

# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_deluxe_rooms = [r for r in deluxe_rooms if r.id % 2 == 0]
    return '\n'.join(str(r) for r in even_deluxe_rooms)

# print(get_deluxe_rooms())


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for r in rooms:
        if not rooms.is_reserved:
            continue

        if previous_room_capacity is not None:
            r.capacity += previous_room_capacity
        else:
            r.capacity += r.id
        previous_room_capacity = r.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)


def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )
    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )
    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character):
    fusion_name = first_character.name + ' ' + second_character.name
    fusion_class_name = 'Fusion'
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    fusion_hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ['Mage', 'Scout']:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=fusion_name,
        class_name=fusion_class_name,
        level=fusion_level,
        strength=fusion_strength,
        dexterity=fusion_dexterity,
        intelligence=fusion_intelligence,
        hit_points=fusion_hit_points,
        inventory=fusion_inventory
    )

    first_character.delete()
    second_character.delete()


# character1 = Character.objects.create(
#     name='Gandalf',
#     class_name='Mage',
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory='Staff of Magic, Spellbook',
# )
#
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )

# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()
