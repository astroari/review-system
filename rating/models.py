from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    order_id = models.CharField(max_length=6, unique=True)
    rating = models.IntegerField(default=0,
            validators=[
                MaxValueValidator(5),
                MinValueValidator(0)
            ])
    review = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    branch_id = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.pk)
