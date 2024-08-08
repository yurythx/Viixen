from django.shortcuts import render

def blog_index(request):
    return render(request, 'blog_index.html')



def blog_details(request):
    return render(request, 'blog_details.html')

