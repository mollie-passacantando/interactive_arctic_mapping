from django.shortcuts import render
from django.http import HttpResponse
from utils.response import response
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'home.html')


@csrf_exempt
def output(request):
    data = response()
    return render(request,'home.html',{'data':data})
    # return render(request,'home.html',data)
    # return HttpResponse(data)