# Generated by Django 3.2.15 on 2022-09-08 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polling_station', '0002_auto_20220908_0836'),
        ('voter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterimage',
            name='polling_station',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='voter_images', to='polling_station.pollingstation'),
            preserve_default=False,
        ),
    ]