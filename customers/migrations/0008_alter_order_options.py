# Generated by Django 4.1.2 on 2022-10-31 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_alter_order_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Order'},
        ),
    ]
