from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['order_id', 'rating', 'review', 'date_added', 'branch_id']
