import csv
import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'medrecord/index.html')


def save_patient(request):
    if request.method == "POST":
        try:
            save_request_data(request)
        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
    return render(request, 'medrecord/save_patient.html')


def save_request_data(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    pesel = request.POST.get('pesel')
    if len(pesel) != 11:
        raise ValueError("PESEL length must be 11")
    chronic_conditions = request.POST.get('chronic_conditions')
    file_path = request.POST.get('file_path')
    if not os.path.isfile(file_path) and '.csv' not in file_path:
        raise FileNotFoundError('No such a csv file')

    patient = [first_name, last_name, pesel, chronic_conditions]

    with open(file_path, mode='a') as record_file:
        record_file = csv.writer(record_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        record_file.writerow(patient)
    return


def open_patient(request):
    return render(request, 'medrecord/open_patient.html')


def opened_record(request):
    print(request)
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        print('file_path')
        print(file_path)
        if not os.path.isfile(file_path) and '.csv' not in file_path:
            raise FileNotFoundError('No such a csv file')

        with open(file_path, mode='r') as record_file:
            record_file = csv.reader(record_file, delimiter=',', quotechar='"')
            record = []
            for row in record_file:
                row_dict = {
                    'first_name': row[0],
                    'last_name': row[1],
                    'pesel': row[2],
                    'clinics': row[3],
                    'chronic_conditions': row[4]
                }
                record.append(row_dict)
                print(row_dict)
        return render(request, 'medrecord/opened_record.html', {'record': record})

    return render(request, 'medrecord/opened_record.html')
