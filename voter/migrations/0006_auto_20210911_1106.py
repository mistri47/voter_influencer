# Generated by Django 3.1.13 on 2021-09-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0005_pollingagent'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='category',
            field=models.CharField(blank=True, choices=[('GENERAL', 'GENERAL'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='voter',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
