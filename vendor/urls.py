from django.urls import path
from .views import VendorAPI
from history_performance.views import VendorPerformanceAPIView

urlpatterns = [
    path('', VendorAPI.as_view(), name='vendor-list'),
    path('<int:vendor_id>/', VendorAPI.as_view(), name='vendor-detail'),
    path('<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]