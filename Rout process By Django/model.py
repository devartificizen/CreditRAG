from django.db import models

# Create your models here.
from django.db import models

class DisputeRequest(models.Model):
    payment_status = models.IntegerField()
    account_status = models.CharField(max_length=50)
    creditor_remark = models.TextField()
    dispute_letter_generated = models.BooleanField(default=False)
