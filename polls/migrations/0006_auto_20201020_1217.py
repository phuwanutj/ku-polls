# Generated by Django 3.1 on 2020-10-20 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_choice_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='selected_choice',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='polls.choice'),
        ),
    ]
