# Generated by Django 3.1 on 2020-10-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_choice_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
