# Generated by Django 3.1 on 2020-10-22 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20201021_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='last_vote',
        ),
    ]
