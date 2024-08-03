import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission


# Create queries within functions
# 4.

def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    query = (Q(name__icontains=search_string) | Q(phone_number__icontains=search_string))

    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts:
        return ''

    result = []

    for astronaut in astronauts:
        result.append(f'Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: '
                      f'{"Active" if astronaut.is_active == True else"Inactive"}')

    return '\n'.join(result)

# print(get_astronauts('123'))


def get_top_astronaut():
    if not Mission.objects.all():
        return "No data."

    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not top_astronaut:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."

# print(get_top_astronaut())


def get_top_commander():
    if not Mission.objects.all():
        return "No data."

    commander = (Astronaut.objects.annotate(missions_count=Count('commanded_missions'))
                 .order_by('-missions_count', 'phone_number')
                 .first()
                 )

    if not commander or commander.missions_count == 0:
        return "No data."

    return f"Top Commander: {commander.name} with {commander.missions_count} commanded missions."

# print(get_top_commander())


# 5.
def get_last_completed_mission():
    mission = Mission.objects.prefetch_related('astronauts').filter(status='Completed').order_by('-launch_date').first()

    if not mission:
        return 'No data.'

    commander = mission.commander.name if mission.commander else 'TBA'

    astronauts = mission.astronauts.all().order_by('name')
    astronauts_names = ", ".join(astronaut.name for astronaut in astronauts)

    total_spacewalks = astronauts.aggregate(spacewalks_sum=Sum('spacewalks'))

    return (f'The last completed mission is: {mission.name}. Commander: {commander}. '
            f'Astronauts: {astronauts_names}. Spacecraft: {mission.spacecraft.name}. '
            f'Total spacewalks: {total_spacewalks["spacewalks_sum"]}.')

# print(get_last_completed_mission())


def get_most_used_spacecraft():
    if not Mission.objects.all():
        return 'No data.'

    spacecraft = (Spacecraft.objects.prefetch_related('missions')
                  .annotate(missions_count=Count('missions__id'))
                  .order_by('-missions_count', 'name')
                  .first()
                  )

    if not spacecraft:
        return 'No data.'

    num_of_astronauts = (Mission.objects.filter(spacecraft=spacecraft)
                         .values('astronauts')
                         .distinct()
                         .count()
                         )

    return (f'The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, '
            f'used in {spacecraft.missions_count} missions, astronauts on missions: '
            f'{num_of_astronauts}.')

# print(get_most_used_spacecraft())


def decrease_spacecrafts_weight():
    spacecrafts = (Spacecraft.objects.filter(missions__status='Planned', weight__gte=200.0)
                   .distinct()
                   )

    if not spacecrafts:
        return "No changes in weight."

    for spacecraft in spacecrafts:
        spacecraft.weight -= 200
        spacecraft.save()

    num_of_spacecrafts = spacecrafts.count()
    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))

    return (f'The weight of {num_of_spacecrafts} spacecrafts has been decreased. '
            f'The new average weight of all spacecrafts is {avg_weight["avg_weight"]:.1f}kg')

# print(decrease_spacecrafts_weight())
