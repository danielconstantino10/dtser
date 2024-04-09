from django.shortcuts import render

# Create your views here.


def home_index(request):
    template_name = 'home/index.html'
    data = {}
    return render (request, template_name, data)

def about(request):
    template_name = 'home/about.html'
    data = {}
    return render (request, template_name, data)