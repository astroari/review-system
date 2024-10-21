from django.shortcuts import render
from .models import Review

def main_view(request):
    context = {
        
    }
    return render(request, 'rating/main.html', context)