# Generated by Django 5.1.2 on 2024-10-12 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_image_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
