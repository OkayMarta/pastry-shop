# Generated by Django 5.1.6 on 2025-05-10 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_order_product_type_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.PROTECT, to='shop.assortmentitem', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
