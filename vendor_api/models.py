
# vendor_api/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from functools import partial

def validate_not_empty(value,field_name):
    """
     Custom Validations:
        - `validate_not_empty`: Function ensures that the value can not be empty.
    """

    if not value:
        raise ValidationError(f"{field_name} cannot be empty")

    

def validate_alphanumeric(value):       
    """
     Custom Validations:
        - `validate_alphanumeric`: Function ensures that the value should be alphanumeric character.
    """

    if not all(char.isalnum() or char.isspace() for char in value):
        raise ValidationError("Name should only contain alphanumeric characters or spaces")  
    
        

class Vendor(models.Model):

    """
    Model representing a vendor.

    Attributes:
        name (str): The name of the vendor.
        contact_details (str): The contact details of the vendor.
        address (str): The address of the vendor.
        vendor_code (str): A unique identifier for the vendor.
        on_time_delivery_rate (float): The on-time delivery rate of the vendor, ranging from 0 to 100.
        quality_rating_avg (float): The average quality rating of the vendor, ranging from 0 to 5.
        average_response_time (float): The average response time of the vendor in hours.
        fulfillment_rate (float): The fulfillment rate of the vendor, ranging from 0 to 1.
         
    """        

    name = models.CharField(max_length=50, validators=[
        partial(validate_not_empty, field_name='Name'),
        validate_alphanumeric
    ])
    contact_details = models.TextField(validators=[
        partial(validate_not_empty, field_name='Contact Details')
    ])
    address = models.TextField(validators=[
        partial(validate_not_empty, field_name='Address')
    ])
    vendor_code = models.CharField(max_length=50, unique=True, validators=[
        partial(validate_not_empty, field_name='Vendor Code')
    ])
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)




class PurchaseOrder(models.Model):
    """
    Model representing a purchase order.

    Attributes:
        vendor (ForeignKey): Reference to the Vendor model.
        po_number (CharField): Unique identifier for the purchase order.
        order_date (DateTimeField): Date when the order was placed.
        delivery_date (DateTimeField): Date when the order is expected to be delivered.
        items (JSONField): JSON representation of the items in the purchase order.
        quantity (IntegerField): Quantity of items in the purchase order.
        status (CharField): Current status of the purchase order (default is 'pending').
        quality_rating (FloatField): Quality rating for the purchase order.
        issue_date (DateTimeField): Date when an issue occurred with the order.
        acknowledgment_date (DateTimeField, optional): Date when the order was acknowledged.

    """

    



    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=20, unique=True,validators=[
        partial(validate_not_empty, field_name='PO Number')
    ])
    order_date = models.DateTimeField(validators=[
        partial(validate_not_empty, field_name='Order Date')
    ])
    delivery_date = models.DateTimeField(validators=[
        partial(validate_not_empty, field_name='Delivery Date')
    ])
    items = models.JSONField(validators=[
        partial(validate_not_empty, field_name='Items')
    ])
    quantity = models.IntegerField(validators=[
        partial(validate_not_empty, field_name='Quantity')
    ])
    status = models.CharField(max_length=50, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(validators=[
        partial(validate_not_empty, field_name='Issue Date')
    ])
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


 

class HistoricalPerformance(models.Model):
    """
    Model representing Historical Performance

        This model optionally stores historical data on vendor performance, enabling trend analysis

    Attributes:
        vendor: (ForeignKey) - Link to the Vendor model.
        date: (DateTimeField) - Date of the performance record.
        on_time_delivery_rate: (FloatField) - Historical record of the on-time delivery rate.
        quality_rating_avg: (FloatField) - Historical record of the quality rating average.
        average_response_time: (FloatField) - Historical record of the average response time.
        fulfillment_rate: (FloatField) - Historical record of the fulfilment rate
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

