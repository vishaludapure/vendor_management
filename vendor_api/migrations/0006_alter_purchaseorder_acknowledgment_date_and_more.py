# Generated by Django 4.2.7 on 2023-11-30 09:03

from django.db import migrations, models
import functools
import vendor_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_api', '0005_alter_purchaseorder_acknowledgment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(validators=[functools.partial(vendor_api.models.validate_not_empty, *(), **{'field_name': 'Delivery Date'})]),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateTimeField(validators=[functools.partial(vendor_api.models.validate_not_empty, *(), **{'field_name': 'Issue Date'})]),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateTimeField(validators=[functools.partial(vendor_api.models.validate_not_empty, *(), **{'field_name': 'Order Date'})]),
        ),
    ]
