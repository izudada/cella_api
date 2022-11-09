# Generated by Django 3.2.16 on 2022-11-09 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cella', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='price_ht',
            new_name='price',
        ),
        migrations.AlterField(
            model_name='cart',
            name='pkid',
            field=models.UUIDField(default='000000', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='pkid',
            field=models.UUIDField(default='000000', editable=False, primary_key=True, serialize=False),
        ),
    ]