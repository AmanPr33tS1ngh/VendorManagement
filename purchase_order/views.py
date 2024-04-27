from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from django.db.models import Q

class PurchaseOrderAPI(APIView):
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        query = Q() if vendor_id else Q(vendor_id=vendor_id)
        purchase_orders = PurchaseOrder.objects.filter(query)
        
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderWithPOIdAPI(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if purchase_order:
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        return Response({"message": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if purchase_order:
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if purchase_order:
            purchase_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
