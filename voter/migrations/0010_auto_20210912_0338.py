# Generated by Django 3.1.13 on 2021-09-12 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0009_pollingstationimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollingstationimage',
            name='h',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pollingstationimage',
            name='w',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pollingstationimage',
            name='x',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pollingstationimage',
            name='y',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]