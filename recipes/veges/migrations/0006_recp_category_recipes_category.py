# Generated by Django 5.0.4 on 2024-05-14 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veges', '0005_recipes_favourites_recipes_ratings_recipes_views_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='recp_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='recipes',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='veges.recp_category'),
        ),
    ]
