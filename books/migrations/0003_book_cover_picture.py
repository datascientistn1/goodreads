# Generated by Django 4.1.5 on 2023-01-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(default='default_cover.jpg', upload_to=''),
        ),
    ]
