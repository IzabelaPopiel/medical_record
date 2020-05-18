from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'medrecord/index.html')
    # return HttpResponse("Index")


def save_patient(request):
    return render(request, 'medrecord/save_patient.html')


def open_patient(request):
    response = "You're opening patient."
    return HttpResponse(response)


