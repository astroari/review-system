from django.db import models


class Review(models.Model):
    order_id = models.CharField(max_length=6, unique=True)
    # rating = models.IntegerField(max_length=1)
    review = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
