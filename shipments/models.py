from django.db import models

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=50)
    carrier = models.CharField(max_length=50)
    sender_address = models.TextField()
    receiver_address = models.TextField()
    article_name = models.CharField(max_length=100)
    article_quantity = models.PositiveIntegerField()
    article_price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.tracking_number} ({self.carrier})"
