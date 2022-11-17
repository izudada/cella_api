# Generated by Django 3.2.16 on 2022-11-16 18:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cella', '0004_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]