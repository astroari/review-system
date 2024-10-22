from django.shortcuts import render, redirect
from .models import Review
from django.http import JsonResponse
from django.db import IntegrityError
import requests
from django.urls import reverse

def main_view(request):
    context = {
        
    }
    return render(request, 'rating/main.html', context)

from django.http import JsonResponse
from django.urls import reverse

def rate_view(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        review = request.POST.get('review')
        
        # Check if a review already exists
        if Review.objects.filter(order_id=el_id).exists():
            return JsonResponse({
                'success': 'false',
                'error': 'A review for this order already exists'
            }, safe=False)
        
        # Check if the order ID is valid -> exists in the order system
        # make an api request to the order system with the order id we got
        order_data = call_order_system(el_id)
        # if the order id is not found, return an error
        if order_data['stateCode'] != 200:
            return JsonResponse({
                'success': 'false',
                'error': 'Order not found or not delivered yet'
            }, safe=False)
        # if the order id is found then check that the status is over or equal to 4
        # if the status is less than 4 return an error
        # if the status is 4 or more, save the review   
        
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
    

def call_order_system(order_id):
    url = "https://crm.eman.uz/v1/api/get-delivery-info"
    payload = {'id': order_id}
    headers = {
        'token': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
