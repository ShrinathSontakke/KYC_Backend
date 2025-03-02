# filepath: /e:/Code/New folder/KYC_Backend/KYC_Backend/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')