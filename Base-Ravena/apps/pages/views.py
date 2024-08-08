from django.shortcuts import render

def index(request):
    return render(request, 'index.html')



def error404(request):
    return render(request, 'varios/error404.html')

def error500(request):
    return render(request, 'varios/error500.html')

