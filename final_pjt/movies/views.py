from django.shortcuts import render


# Create your views here.
def movie_detail(request):
    pass

def movie_like(request):
    pass

def index(request):
    return render(request, 'movies/index.html')

