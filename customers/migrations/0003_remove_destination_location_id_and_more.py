# Generated by Django 4.1.2 on 2022-11-02 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_destination_location_street_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination_location',
            name='id',
        ),
        migrations.AlterField(
            model_name='destination_location',
            name='street_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vehicle_list',
            name='street_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_list', to='customers.destination_location'),
        ),
    ]
