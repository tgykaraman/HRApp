# Generated by Django 5.0.8 on 2024-08-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hr_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="absence",
            field=models.DecimalField(decimal_places=1, default=7.0, max_digits=4),
        ),
    ]
