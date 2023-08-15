# Generated by Django 3.2 on 2023-08-08 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230807_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_amount', to='recipes.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_amount', to='recipes.recipe'),
        ),
    ]
