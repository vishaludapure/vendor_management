# vendor_api/views.py
from rest_framework import generics
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, status



class VendorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating Vendor instances.

    Permissions:
    - User must be authenticated.

    GET:
    - Retrieve a list of all vendors.

    POST:
    - Create a new vendor.

    Request Body (JSON):
    {
        "name": "Vendor Name",
        "contact_details": "Contact Details",
        "address": "Vendor Address",
        "vendor_code": "Unique Vendor Code"
    }
    """
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer



class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific Vendor instance.

    Permissions:
    - User must be authenticated.

    GET:
    - Retrieve details of a specific vendor.

    PUT/PATCH:
    - Update details of a specific vendor.

    DELETE:
    - Delete a specific vendor.
    """
    permission_classes = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating PurchaseOrder instances.

    Permissions:
    - User must be authenticated.

    GET:
    - Retrieve a list of all purchase orders.

    POST:
    - Create a new purchase order.

    Request Body (JSON):
    {
        "vendor": 1,
        "po_number": "Unique PO Number",
        "order_date": "2023-01-01T12:00:00Z",
        "delivery_date": "2023-01-10T12:00:00Z",
        "items": [items details in json format],
        "quantity": 10
    }
    """
    permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderListView(generics.ListAPIView):
    """
    API view for listing PurchaseOrder instances based on vendor_id.

    Permissions:
    - User must be authenticated.

    GET:
    - Retrieve a list of purchase orders based on a vendor ID.

    Query Parameters:
    - vendor_id (int): The ID of the vendor for filtering.
    """
    permission_classes = [IsAuthenticated]

    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor_id')

        if vendor_id is not None:
            try:
                vendor_id = int(vendor_id)
                queryset = queryset.filter(vendor_id=vendor_id)
            except ValueError:
                print("Invalid vendor ID format. Please provide an integer.")

        return queryset


class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific PurchaseOrder instance.

    Permissions:
    - User must be authenticated.

    GET:
    - Retrieve details of a specific purchase order.

    PUT/PATCH:
    - Update details of a specific purchase order.

    DELETE:
    - Delete a specific purchase order.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'po_number'
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Check if the po_number is being updated
        new_po_number = request.data.get('po_number')
        if new_po_number and new_po_number != instance.po_number:
            # Check if there's any other PurchaseOrder with the same po_number
            if PurchaseOrder.objects.filter(po_number=new_po_number).exclude(pk=instance.pk).exists():
                return Response({"po_number": ["PO number must be unique."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)




class PurchaseOrderAcknowledgeView(generics.UpdateAPIView):
    """
    API view for updating the acknowledgment_date of a PurchaseOrder instance.

    Permissions:
    - User must be authenticated.

    PUT:
    - Update the acknowledgment_date of a specific purchase order.

    Request Body (JSON):
    {
        "acknowledgment_date": "2023-01-05T12:00:00Z"
    }
    """
    permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'

    def put(self, request, *args, **kwargs):
        # Perform the update using the generic update view
        return self.update(request, *args, **kwargs)

class VendorPerformanceView(generics.RetrieveAPIView):
    """
    API view for retrieving performance metrics of a specific Vendor instance.

    GET:
    - Retrieve performance metrics of a specific vendor.

    """


    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Round the quality_rating_avg to a single decimal point
        quality_rating_avg_rounded = instance.quality_rating_avg

        # If quality_rating_avg is not None, round it to a single decimal point
        if quality_rating_avg_rounded is not None:
            quality_rating_avg_rounded = round(quality_rating_avg_rounded, 1)

        serializer = self.get_serializer(instance)

        # Send real-time update to WebSocket consumers
        self.send_realtime_update({
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg_rounded,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate,
        })

        return Response({
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg_rounded,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate,
        })

    def send_realtime_update(self, performance_data):
        channel_layer = get_channel_layer()

        # Send update to the VendorPerformanceConsumer
        async_to_sync(channel_layer.group_send)(
            'vendor_performance_group',
            {
                'type': 'update_vendor_performance',
                'performance_data': performance_data,
            }
        )