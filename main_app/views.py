from django.shortcuts import render, redirect
import uuid
import boto3
import os
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy , Photo
from .forms import FeedingForm

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
    # create list of toys ids that cat has 
    id_list = cat.toys.all().values_list('id')
      # Now we can query for toys whose ids are not in the list using exclude
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request,'cats/detail.html',{
        'cat': cat,
        'feeding_form': feeding_form,
        "toys": toys_cat_doesnt_have
        })

class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # fields = '__all__'
    # success_url = '/cats/{cat.id}'

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed','description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'


def add_feeding(request,cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail',cat_id=cat_id)

class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
    

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'


def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

def remove_toy(request,cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail',cat_id=cat_id)

def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
              # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print("An error occured uploading file to S3")
            print(e)
    return redirect('detail', cat_id=cat_id)

