from django.db import models

# Create your models here.

class TransportOrder(models.Model):
    order_number = models.CharField(max_length=500)
    customer_name = models.CharField(max_length=500)
    date = models.DateField()

class Waypoint(models.Model):
    transport_order = models.ForeignKey(TransportOrder, related_name='waypoints', on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255)
    TYPE_CHOICES = [
        ('Pickup', 'Pickup'),
        ('Delivery', 'Delivery')
    ]
    waypoint_type = models.CharField(max_length=20, choices=TYPE_CHOICES)