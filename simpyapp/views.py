from django.http import HttpResponse
from django.shortcuts import render
from simpyapp.algorithm.sim import Sim


def index(request):
    return render(request, 'index.html')


def compare(request):
    doc1 = request.POST.get('doc1')
    doc2 = request.POST.get('doc2')
    sim = Sim()
    v = sim.compare([doc1, doc2])
    if v == -1:
        s = 'Too simple'
    else:
        s = '{:.2f}%'.format(v * 100)
    return HttpResponse(s)
