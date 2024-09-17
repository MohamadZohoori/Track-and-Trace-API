from django.urls import path
from .views import shipment_detail

urlpatterns = [
    path('shipments/<str:carrier>/<str:tracking_number>/', shipment_detail),
]
