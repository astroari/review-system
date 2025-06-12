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
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.utils import timezone
from datetime import datetime
from django.http import Http404
def main_view(request, prefilled_order_id=None, prefilled_phonenumber=None):
    # Check if the order_id and phone number are valid together
    # If not valid, redirect to 400 page
    if prefilled_order_id and prefilled_phonenumber:
        order_data = call_order_system(prefilled_order_id)
        if order_data['stateCode'] != 200 or order_data['orders'][0]['phone'] != prefilled_phonenumber:
            return HttpResponseBadRequest()
    
    context = {
        'prefilled_order_id': prefilled_order_id,
        'prefilled_phonenumber': prefilled_phonenumber
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
                'error': _('A review for this order already exists')
            }, safe=False)
        
        # Check if the order ID is valid -> exists in the order system and is at the review stage
        order_data = call_order_system(el_id)
        if order_data['stateCode'] != 200 or order_data['orders'][0]['status'] < 4:
            return JsonResponse({
                'success': 'false',
                'error': _('Order not found or not available for review')
            }, safe=False)
        
        # Save order's branch id
        branch_id = order_data['orders'][0]['branch_id']
        
        try:
            review = Review(order_id=el_id, rating=val, review=review, branch_id=branch_id)
            review.save()
            return JsonResponse({
                'success': 'true',
                'redirect_url': reverse('success-view')
            })
        except IntegrityError:
            return JsonResponse({
                'success': 'false',
                'error': _('An error occurred while saving the review')
            }, safe=False)
    else:
        return JsonResponse({'success': 'false'}, safe=False)
    


def success_view(request):
    context = {
        'main_view_url': reverse('main-view'),
        'eman_website_url': 'https://eman.uz/'
    }
    return render(request, 'rating/success.html', context)
    
def custom_bad_request_view(request, exception):
    return render(request, '400.html', status=400)

def call_order_system(order_id):
    url = "http://192.168.183.20/v1/api/get-orders-info"
    # url = "https://crm.eman.uz/v1/api/get-orders-info"
    headers = {
        'token': settings.CRM_KEY
    }

    response = requests.request("GET", url+f"?id={order_id}", headers=headers)
    return response.json()

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Review.objects.all()
        
        # Order ID filter
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order_id=order_id)
            if not queryset.exists():
                raise NotFound(_(f"No review found for order_id: {order_id}"))
        
        # Date range filter
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        try:
            if start_date:
                start_datetime = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
                queryset = queryset.filter(date_added__gte=start_datetime)
            if end_date:
                end_datetime = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1))
                queryset = queryset.filter(date_added__lt=end_datetime)
        except ValueError:
            raise Http404(_("Invalid date format"))
            
        return queryset

from rest_framework.response import Response
from rest_framework import serializers

class CustomerServiceReviewView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Review.objects.all()
        
        # Order ID filter
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order_id=order_id)
            if not queryset.exists():
                raise NotFound(_(f"No review found for order_id: {order_id}"))
        
        # Date range filter
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        try:
            if start_date:
                start_datetime = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
                queryset = queryset.filter(date_added__gte=start_datetime)
            if end_date:
                end_datetime = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1))
                queryset = queryset.filter(date_added__lt=end_datetime)
        except ValueError:
            raise Http404(_("Invalid date format"))
            
        return queryset

    def get_serializer_class(self):
        class EnrichedReviewSerializer(self.serializer_class):
            branch_id = serializers.CharField(read_only=True)
            phone_number = serializers.CharField(read_only=True)
            
            class Meta(self.serializer_class.Meta):
                fields = list(self.serializer_class.Meta.fields) + ['branch_id', 'phone_number']

        return EnrichedReviewSerializer

    def list(self, request, *args, **kwargs):
        reviews = self.get_queryset()
        enriched_reviews = []
        
        for review in reviews:
            order_data = call_order_system(review.order_id)
            review_data = self.get_serializer(review).data
            if order_data['stateCode'] == 200:
                review_data['branch_id'] = order_data["orders"][0]["branch_id"]
                review_data['phone_number'] = order_data["orders"][0]["phone"]
            enriched_reviews.append(review_data)

        return Response(enriched_reviews)

def translate(language, text):
    cur_language = get_language()
    try:
        activate(language)
        return gettext(text)
    finally:
        activate(cur_language)
    return text
