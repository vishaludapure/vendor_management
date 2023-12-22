# vendor_api/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor_api.models import PurchaseOrder, Vendor, HistoricalPerformance
from django.db.models import Count, Avg, ExpressionWrapper, F, fields
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


logger = logging.getLogger(__name__)


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_on_time_delivery_rate(sender, instance, **kwargs):
    """
    Update the on-time delivery rate for the vendor when a PurchaseOrder is completed.
    """
    try:
      
        # Count the number of completed PurchaseOrders for the vendor
        completed_orders_count = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            delivery_date__lte=F('acknowledgment_date')   
        ).count()

      
       
        # Count all completed PurchaseOrders for all vendors
        completed_orders_count_all_vendors = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        ).count()

       
       

        # Calculate on-time delivery rate for the specific vendor
        on_time_delivery_rate_vendor = (
            completed_orders_count / completed_orders_count_all_vendors
        ) if completed_orders_count_all_vendors > 0 else 0

        # Update the Vendor model with the calculated on_time_delivery_rate
        instance.vendor.on_time_delivery_rate = on_time_delivery_rate_vendor
        instance.vendor.save()
        


            # Prepare the updated data
        updated_data = {
            
            "initial_performance_data": {
                "on_time_delivery_rate": instance.vendor.on_time_delivery_rate,
                "quality_rating_avg": instance.vendor.quality_rating_avg,
                "average_response_time": instance.vendor.average_response_time,
                "fulfillment_rate": instance.vendor.fulfillment_rate
            }
        }


        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'vendor_performance_group',
            {
                'type': 'signal_receive_handler',
                'data': updated_data,
            }
        )
    
    except Exception as e:
        # Log the exception
        logger.error(f"Exception in update_vendor_on_time_delivery_rate: {str(e)}")



@receiver(post_save, sender=PurchaseOrder)
def update_vendor_quality_rating_avg(sender, instance, **kwargs):
    """
    Update the average quality rating for the vendor when a PurchaseOrder with a rating is completed.
    """
    try:
        # Check if the quality_rating is provided and the status is 'completed'
        if instance.quality_rating is not None and instance.status == 'completed':
            # Get all completed PurchaseOrders with a quality_rating for the vendor
            completed_orders_with_rating = PurchaseOrder.objects.filter(
                vendor=instance.vendor,
                status='completed',
                quality_rating__isnull=False
            )

            # Calculate the average quality_rating for completed PurchaseOrders
            quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

            # Update the Vendor model with the calculated quality_rating_avg
            instance.vendor.quality_rating_avg = quality_rating_avg
            instance.vendor.save()

            updated_data = {
               
                "initial_performance_data": {
                    "on_time_delivery_rate": instance.vendor.on_time_delivery_rate,
                    "quality_rating_avg": instance.vendor.quality_rating_avg,
                    "average_response_time": instance.vendor.average_response_time,
                    "fulfillment_rate": instance.vendor.fulfillment_rate
                }
            }

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'vendor_performance_group',
                {
                    'type': 'signal_receive_handler',
                    'data': updated_data,
                }
            )
    except Exception as e:
        # Log the exception
        logger.error(f"Exception in update_vendor_quality_rating_avg: {str(e)}")



@receiver(post_save, sender=PurchaseOrder)
def update_vendor_average_response_time(sender, instance, **kwargs):
    """
    Update the average response time for the vendor when a PurchaseOrder is acknowledged.
    """
    try:
      
        # Get all completed PurchaseOrders with acknowledgment_date for the vendor
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            acknowledgment_date__isnull=False
        )

        # Calculate the average response time for completed PurchaseOrders
        response_times = acknowledged_orders.annotate(
            response_time=models.ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=models.DurationField()
            )
        ).aggregate(Avg('response_time'))['response_time__avg'] or 0

        # Update the Vendor model with the calculated average response time
        instance.vendor.average_response_time = response_times.total_seconds() / 3600  # Convert to hours
        instance.vendor.save()
        

        updated_data = {
         
            "initial_performance_data": {
                "on_time_delivery_rate": instance.vendor.on_time_delivery_rate,
                "quality_rating_avg": instance.vendor.quality_rating_avg,
                "average_response_time": instance.vendor.average_response_time,
                "fulfillment_rate": instance.vendor.fulfillment_rate
            }
        }


        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'vendor_performance_group',
            {
                'type': 'signal_receive_handler',
                'data': updated_data,
            }
        )
    except Exception as e:
        # Log the exception
        logger.error(f"Exception in update_vendor_average_response_time: {str(e)}")



@receiver(post_save, sender=PurchaseOrder)
def update_vendor_fulfillment_rate(sender, instance, **kwargs):
    """
    Update the fulfillment rate for the vendor upon any change in PurchaseOrder status.
    """
    try:
       
       
       # Count the number of successfully fulfilled PurchaseOrders (status 'completed' without issues) for the specific vendor
        fulfilled_orders_count = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        ).count()

        # Count all PurchaseOrders issued to the specific vendor (regardless of status)
        total_orders_count_for_vendors = PurchaseOrder.objects.filter(
            vendor=instance.vendor
        ).count()

        # Calculate fulfillment rate for the specific vendor
        fulfillment_rate_vendor = fulfilled_orders_count / total_orders_count_for_vendors if total_orders_count_for_vendors > 0 else 0

        # Update the Vendor model with the calculated fulfillment rate
        instance.vendor.fulfillment_rate = fulfillment_rate_vendor
        instance.vendor.save()


        updated_data = {
           
            "initial_performance_data": {
                "on_time_delivery_rate": instance.vendor.on_time_delivery_rate,
                "quality_rating_avg": instance.vendor.quality_rating_avg,
                "average_response_time": instance.vendor.average_response_time,
                "fulfillment_rate": instance.vendor.fulfillment_rate
            }
        }


        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'vendor_performance_group',
            {
                'type': 'signal_receive_handler',
                'data': updated_data,
            }
        )

    except Exception as e:
        # Log the exception
        logger.error(f"Exception in update_vendor_fulfillment_rate: {str(e)}")



@receiver(post_save, sender=Vendor)
def update_vendor_historical_performance(sender, instance, **kwargs):
    """
    Update historical performance for the vendor upon any change in Vendor data.
    """
    try:
        # Get or create the HistoricalPerformance entry for the vendor and current date
        historical_entry, created = HistoricalPerformance.objects.get_or_create(
            vendor=instance,
            date=timezone.now().date(),
        )

        # Update historical data based on Vendor model
        historical_entry.on_time_delivery_rate = instance.on_time_delivery_rate
        historical_entry.quality_rating_avg = instance.quality_rating_avg
        historical_entry.average_response_time = instance.average_response_time
        historical_entry.fulfillment_rate = instance.fulfillment_rate

        # Save the changes to HistoricalPerformance Model
        historical_entry.save()

    except ValidationError as ve:
        # Log validation error
        logger.error(f"Validation error in update_vendor_historical_performance: {ve}")
    except Exception as e:
        # Log other exceptions
        logger.error(f"Exception in update_vendor_historical_performance: {str(e)}")

