# Generated by Django 3.1 on 2020-10-20 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20201020_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='selected_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.choice'),
        ),
    ]
