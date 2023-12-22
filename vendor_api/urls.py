# vendor_api/urls.py
from django.urls import path
from .views import PurchaseOrderAcknowledgeView, PurchaseOrderListView, VendorListCreateView, VendorRetrieveUpdateDeleteView, \
    PurchaseOrderListCreateView, PurchaseOrderRetrieveUpdateDeleteView, VendorPerformanceView

from django.urls import re_path
from .views import PurchaseOrderListView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('api/vendors/<int:id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),

    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<str:po_number>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
    path('api/purchase_orders/<str:po_number>/acknowledge/', PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge'),

]
