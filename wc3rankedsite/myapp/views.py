# Create your views here.

from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'myapp/book_list.html', {'books': books})

def home(request):
    return render(request, 'myapp/home.html')

def leaderboards(request):
    return render(request, 'myapp/leaderboards.html')

def contact(request):
    return render(request, 'myapp/contact.html')

def about(request):
    return render(request, 'myapp/about.html')
