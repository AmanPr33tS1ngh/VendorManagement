from django.contrib import admin
from .models import Vendor, HistoricalPerformance
# Register your models here.

admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)