# Generated by Django 5.0.4 on 2024-07-30 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_publisher_recommendedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('F', 'Fiction'), ('B', 'Biography'), ('SF', 'Science Fiction'), ('FA', 'Fantasy'), ('MY', 'Mystery'), ('TH', 'Thriller'), ('RO', 'Romance'), ('HO', 'Horror'), ('C', 'Criminal'), ('CL', "Children's literature")], max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]