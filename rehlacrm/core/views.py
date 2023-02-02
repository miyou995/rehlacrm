from django.shortcuts import render, redirect

# Create your views here.
def index_view(request):
    return redirect('admin:index')