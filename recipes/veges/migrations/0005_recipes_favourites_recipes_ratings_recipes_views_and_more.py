# Generated by Django 5.0.4 on 2024-05-14 11:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veges', '0004_tags_recipes_recp_create_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='favourites',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recipes',
            name='ratings',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='recipes',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_text', models.TextField()),
                ('com_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veges.recipes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
