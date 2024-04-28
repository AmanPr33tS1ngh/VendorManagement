from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer

class VendorAPI(APIView):
    def get(self, request, vendor_id=None):
        if vendor_id:
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all vendors
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
