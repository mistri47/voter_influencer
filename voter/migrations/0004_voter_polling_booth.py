# Generated by Django 3.1.13 on 2021-09-11 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0003_auto_20210911_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='polling_booth',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='voter.pollingbooth'),
            preserve_default=False,
        ),
    ]
