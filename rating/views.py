from django.shortcuts import render
from .models import Review
from django.http import JsonResponse
from django.db import IntegrityError

def main_view(request):
    context = {
        
    }
    return render(request, 'rating/main.html', context)

def rate_view(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        
        # Check if a review already exists
        if Review.objects.filter(order_id=el_id).exists():
            return JsonResponse({
                'success': 'false',
                'error': 'A review for this order already exists'
            }, safe=False)
        
        try:
            review = Review(order_id=el_id, rating=val)
            review.save()
            return JsonResponse({'success': 'true', 'score': val}, safe=False)
        except IntegrityError:
            return JsonResponse({
                'success': 'false',
                'error': 'An error occurred while saving the review'
            }, safe=False)
    else:
        return JsonResponse({'success': 'false'}, safe=False)
