# Generated by Django 5.1 on 2024-09-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_furniture_category_furniture_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='furniture',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='furniture',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
