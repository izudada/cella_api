# Generated by Django 3.2.16 on 2022-11-11 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cella', '0010_alter_order_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref',
            field=models.CharField(default='scotch', max_length=50),
        ),
    ]
