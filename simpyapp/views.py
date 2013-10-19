from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def compare(request):
    doc1 = request.POST.get('doc1')
    doc2 = request.POST.get('doc2')
    return HttpResponse(doc1 + doc2)
