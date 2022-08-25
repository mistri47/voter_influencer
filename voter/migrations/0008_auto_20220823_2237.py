# Generated by Django 3.1.13 on 2022-08-23 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0007_auto_20220823_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pollingagent',
            name='category',
            field=models.CharField(blank=True, choices=[('GENERAL', 'GENERAL'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pollingagent',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pollingagent',
            name='mobile',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pollingagent',
            name='agent_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='voter.agenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pollingagent',
            name='caste',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='voter.caste'),
            preserve_default=False,
        ),
    ]