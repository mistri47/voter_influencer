# Generated by Django 3.1.13 on 2022-08-23 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0004_pollingstationimage_boxed_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterimage',
            name='image_url',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]