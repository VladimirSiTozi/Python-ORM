# Generated by Django 5.0.4 on 2024-06-26 21:32

from django.db import migrations


def set_price(apps, schema_editor):
    MULTIPLIER = 120
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    smartphones = smartphone_model.objects.all()

    for smartphone in smartphones:
        smartphone.price = MULTIPLIER * len(smartphone.brand)

    smartphone_model.objects.bulk_update(smartphones, ['price'])


def set_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    smartphones = smartphone_model.objects.all()

    for smartphone in smartphones:
        if smartphone.price >= 750:
            smartphone.category = 'Expensive'
        else:
            smartphone.category = 'Cheap'

    smartphone_model.objects.bulk_update(smartphones, ['category'])


def set_all_columns(apps, schema_editor):
    set_price(apps, schema_editor)
    set_category(apps, schema_editor)


def set_price_and_category_to_default(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    smartphones = smartphone_model.objects.all()

    for smartphone in smartphones:
        smartphone.price = smartphone_model._meta.get_field('price').default
        smartphone.category = smartphone_model._meta.get_field('category').default

    smartphone_model.objects.bulk_update(smartphones, ['price', 'category'])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_smartphone'),
    ]

    operations = [
        migrations.RunPython(set_all_columns, reverse_code=set_price_and_category_to_default)
    ]
