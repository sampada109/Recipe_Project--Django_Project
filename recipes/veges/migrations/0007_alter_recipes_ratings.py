# Generated by Django 5.0.4 on 2024-05-15 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veges', '0006_recp_category_recipes_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
    ]
