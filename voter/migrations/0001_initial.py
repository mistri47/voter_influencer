# Generated by Django 3.1.13 on 2022-08-22 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PollingBooth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.SmallIntegerField()),
                ('address', models.TextField(blank=True, null=True)),
                ('voter_list', models.FileField(blank=True, null=True, upload_to='')),
                ('images_created', models.BooleanField(default=False)),
                ('is_processed', models.BooleanField(default=False)),
                ('has_errors', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PollingStationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='VOTER_LIST', max_length=20)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('page_number', models.SmallIntegerField()),
                ('is_processed', models.BooleanField(default=False)),
                ('has_errors', models.BooleanField(default=False)),
                ('md5_signature', models.CharField(max_length=1000, unique=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='voter.pollingbooth')),
            ],
        ),
        migrations.CreateModel(
            name='VoterImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('is_processed', models.BooleanField(default=False)),
                ('has_errors', models.BooleanField(default=False)),
                ('md5_signature', models.CharField(max_length=1000, unique=True)),
                ('station_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter_images', to='voter.pollingstationimage')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5_signature', models.CharField(max_length=1000, unique=True)),
                ('voter_id', models.CharField(blank=True, max_length=20, null=True)),
                ('serial_number', models.IntegerField(blank=True, null=True)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('husband_name', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.SmallIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=10, null=True)),
                ('house_number', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.CharField(blank=True, choices=[('GENERAL', 'GENERAL'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], max_length=20, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('data_eng', models.TextField(blank=True, null=True)),
                ('data_hin', models.TextField(blank=True, null=True)),
                ('polling_booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='voter.pollingbooth')),
                ('polling_station_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='voter.pollingstationimage')),
                ('voter_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='voter.voterimage')),
            ],
        ),
        migrations.CreateModel(
            name='PollingAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('points', models.IntegerField(default=0)),
                ('polling_booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='voter.pollingbooth')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
