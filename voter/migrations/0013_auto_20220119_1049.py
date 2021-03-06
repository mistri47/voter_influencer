# Generated by Django 3.1.13 on 2022-01-19 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0012_pollingbooth_images_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollingstationimage',
            name='h',
        ),
        migrations.RemoveField(
            model_name='pollingstationimage',
            name='w',
        ),
        migrations.RemoveField(
            model_name='pollingstationimage',
            name='x',
        ),
        migrations.RemoveField(
            model_name='pollingstationimage',
            name='y',
        ),
        migrations.AlterField(
            model_name='voter',
            name='voter_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='VoterImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('station_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter_images', to='voter.pollingstationimage')),
            ],
        ),
    ]
