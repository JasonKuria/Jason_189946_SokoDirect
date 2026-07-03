from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('success',   'Success'),
        ('failed',    'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    user                = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order               = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True)
    phone_number        = models.CharField(max_length=15)
    amount              = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_request_id = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt       = models.CharField(max_length=50, blank=True)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} — {self.status} — {self.phone_number}"
