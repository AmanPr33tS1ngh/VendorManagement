from django.db import models

# Create your models here.
from vendor.models import Vendor
from history_performance.models import HistoricalPerformance
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    print("update_vendor_performance")
    if not created:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = on_time_pos.count() / completed_pos.count() if completed_pos.count() > 0 else 0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={'on_time_delivery_rate': on_time_delivery_rate}
        )

        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating'] or 0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={'quality_rating_avg': quality_rating_avg}
        )

        successful_pos = completed_pos.filter(status='completed', quality_rating__isnull=False)
        fulfillment_rate = successful_pos.count() / PurchaseOrder.objects.filter(vendor=vendor).count() if PurchaseOrder.objects.filter(vendor=vendor).count() > 0 else 0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={'fulfillment_rate': fulfillment_rate}
        )

@receiver(pre_save, sender=PurchaseOrder)
def update_response_time(sender, instance, **kwargs):
    print("update_response_time")
    print(instance.acknowledgment_date, instance.issue_date)
    if instance.acknowledgment_date and instance.issue_date:
        response_time = instance.acknowledgment_date - instance.issue_date
        vendor = instance.vendor
        current_avg_response_time = HistoricalPerformance.objects.filter(vendor=vendor).aggregate(avg_response=models.Avg('average_response_time'))['avg_response'] or 0
        num_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
        new_avg_response_time = (current_avg_response_time * (num_pos - 1) + response_time.total_seconds()) / num_pos if num_pos > 0 else 0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={'average_response_time': new_avg_response_time}
        )