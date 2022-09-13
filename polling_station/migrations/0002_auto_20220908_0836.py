# Generated by Django 3.2.15 on 2022-09-08 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling_station', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollingstation',
            name='female_voters',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pollingstation',
            name='male_voters',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pollingstation',
            name='other_voters',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pollingstation',
            name='total_voters',
            field=models.SmallIntegerField(default=0),
        ),
    ]
