from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def compare(request):
    doc1 = request.POST.get('doc1')
    doc2 = request.POST.get('doc2')
    return HttpResponse(doc1 + doc2)
