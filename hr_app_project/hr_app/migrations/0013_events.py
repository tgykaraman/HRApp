# Generated by Django 5.1 on 2024-08-30 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_app', '0012_alter_salary_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'events',
            },
        ),
    ]
