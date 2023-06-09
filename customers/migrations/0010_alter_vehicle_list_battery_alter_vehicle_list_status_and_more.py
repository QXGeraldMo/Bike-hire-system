# Generated by Django 4.1.2 on 2022-11-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_order_end_alter_order_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle_list',
            name='battery',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='vehicle_list',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vehicle_list',
            name='street_name',
            field=models.CharField(max_length=20),
        ),
    ]
