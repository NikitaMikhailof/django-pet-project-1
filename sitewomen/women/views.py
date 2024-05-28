from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse

def index(request):
    return HttpResponse('Главная страница сайта')

def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категории {cat_id}<h1>')

def categories_by_slug(request, cat_slug):
    if request.POST:
        print(request.POST)
    return HttpResponse(f'<h1>Статьи по категории<h1><p>{cat_slug}<p>')

def archive(request, year):
    if year > 2024:
        uri = reverse('cats', args=('sport', ))
        return HttpResponsePermanentRedirect(uri)
        
    return HttpResponse(f'<h1>Архив по годам <h1><p>{year}<p>')    
    
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не определена<h1>')    