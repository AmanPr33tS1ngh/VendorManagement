from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer
from rest_framework import status

# Create your views here.

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        performances = HistoricalPerformance.objects.filter(vendor=vendor)
        serializer = HistoricalPerformanceSerializer(performances, many=True)
        return Response(serializer.data)