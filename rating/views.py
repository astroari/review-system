from django.shortcuts import render, redirect
from .models import Review
from .serializers import ReviewSerializer
from rest_framework import generics
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.db import IntegrityError
import requests
from django.urls import reverse
from rest_framework.exceptions import NotFound
from django.conf import settings

def main_view(request, prefilled_order_id=None, prefilled_phonenumber=None):
    # Check if the order_id and phone number are valid together
    # If not valid, redirect to 400 page
    if prefilled_order_id and prefilled_phonenumber:
        order_data = call_order_system(prefilled_order_id)
        if order_data['stateCode'] != 200 or order_data['phone'] != prefilled_phonenumber:
            return HttpResponseBadRequest()
    
    context = {
        'order_id': prefilled_order_id
    }
    return render(request, 'rating/main.html', context)

def rate_view(request, prefilled_order_id=None, prefilled_phonenumber=None):
    if request.method == 'POST':
        el_id = request.POST.get('el_id') or prefilled_order_id
        val = request.POST.get('val')
        review = request.POST.get('review')
        
        # Check if a review already exists
        if Review.objects.filter(order_id=el_id).exists():
            return JsonResponse({
                'success': 'false',
                'error': 'A review for this order already exists'
            }, safe=False)
        
        # Check if the order ID is valid -> exists in the order system and is at the review stage
        order_data = call_order_system(el_id)
        if order_data['stateCode'] != 200 or order_data['status'] not in ["Проверка", "Готово", "На складе", "Завершен"]:
            return JsonResponse({
                'success': 'false',
                'error': 'Order not found or not available for review'
            }, safe=False)
        
        try:
            review = Review(order_id=el_id, rating=val, review=review)
            review.save()
            return JsonResponse({
                'success': 'true',
                'redirect_url': reverse('success-view')
            })
        except IntegrityError:
            return JsonResponse({
                'success': 'false',
                'error': 'An error occurred while saving the review'
            }, safe=False)
    else:
        return JsonResponse({'success': 'false'}, safe=False)
    


def success_view(request):
    context = {
        'main_view_url': reverse('main-view')
    }
    return render(request, 'rating/success.html', context)
    
def custom_bad_request_view(request, exception):
    return render(request, '400.html', status=400)

def call_order_system(order_id):
    url = "https://crm.eman.uz/v1/api/get-delivery-info"
    payload = {'id': order_id}
    headers = {
        'token': settings.CRM_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Review.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order_id=order_id)
            if not queryset.exists():
                raise NotFound(f"No review found for order_id: {order_id}")
        return queryset
