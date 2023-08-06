# Generated by Django 4.2.3 on 2023-07-30 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='image',
            field=models.ImageField(default='-', upload_to='images/ingredients/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='-', upload_to='images/recipes/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='custom_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/ingredients/'),
        ),
    ]