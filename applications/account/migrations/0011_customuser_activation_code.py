# Generated by Django 5.1.2 on 2024-11-03 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0010_alter_customuser_img"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="activation_code",
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
