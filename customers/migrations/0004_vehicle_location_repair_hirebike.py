# Generated by Django 4.1.2 on 2022-10-30 12:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_vehicle_location_street_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle_location',
            name='repair',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='HireBike',
            fields=[
                ('session_id', models.IntegerField(primary_key=True, serialize=False)),
                ('departure', models.CharField(max_length=40)),
                ('destination', models.CharField(max_length=40)),
                ('start_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('bike_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.vehicle_location')),
            ],
        ),
    ]
