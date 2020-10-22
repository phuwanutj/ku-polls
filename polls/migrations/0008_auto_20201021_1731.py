# Generated by Django 3.1 on 2020-10-21 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20201020_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='last_vote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set(),
        ),
    ]
