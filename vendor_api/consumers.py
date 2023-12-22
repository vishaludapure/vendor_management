# # your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
import json
from asgiref.sync import sync_to_async

from vendor_api.models import Vendor

class VendorPerformanceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time updates of vendor performance data.

    Attributes:
        vendor_id (int): Identifier for the vendor whose performance data is being tracked.
    """

    async def connect(self):
        """
        Handle WebSocket connection initiation.

        Extracts the vendor ID from the WebSocket URL, adds the connection to the group,
        and sends the  performance data along with a 'connected' message.
        """

        # Extract vendor ID from the WebSocket URL
        self.vendor_id = self.scope['url_route']['kwargs']['id']

        await self.channel_layer.group_add("vendor_performance_group", self.channel_name)
        await self.accept()

        initial_performance_data = await sync_to_async(self.get_initial_performance_data)(self.vendor_id)

        # Send 'connected' message along with initial performance data
        await self.send(text_data=json.dumps({
          
            'initial_performance_data': initial_performance_data,
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("vendor_performance_group", self.channel_name)

   
    def get_initial_performance_data(self, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            initial_data = {
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate,
            }
        except Vendor.DoesNotExist:
            initial_data = {}
        return initial_data
    

    async def signal_receive_handler(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_data',
            'data': event['data'], 
        }))