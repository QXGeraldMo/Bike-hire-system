# Generated by Django 4.1.2 on 2022-11-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination_location',
            name='street_id',
            field=models.IntegerField(default=1),
        ),
    ]