# Generated by Django 3.0.7 on 2021-02-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_changer', '0002_auto_20210226_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='picture',
            field=models.ImageField(upload_to=''),
        ),
    ]