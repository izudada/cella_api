# Generated by Django 3.2.16 on 2022-11-10 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cella', '0006_auto_20221110_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='item_id',
        ),
    ]