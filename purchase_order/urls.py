from django.urls import path
from .views import PurchaseOrderAPI, PurchaseOrderWithPOIdAPI

urlpatterns = [
    path('', PurchaseOrderAPI.as_view(), name='purchaseorder-list-create'),
    path('<int:po_id>/', PurchaseOrderWithPOIdAPI.as_view(), name='purchaseorder-with-po-id'),
]