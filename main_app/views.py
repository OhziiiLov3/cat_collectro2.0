from django.shortcuts import render

from .models import Cat

# Create your views here.
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
# ]

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {
        'cats': cats
    });

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request,'cats/detail.html',{'cat': cat})


