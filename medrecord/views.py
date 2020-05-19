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
            messages.success(request, "Data saved successfully")

        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
    return render(request, 'medrecord/save_patient.html')


def save_request_data(request):
    print(request)
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    pesel = request.POST.get('pesel')
    if len(pesel) != 11:
        raise ValueError("PESEL length must be 11")
    clinics = []
    if 'cardiology' in request.POST:
        clinics.append(request.POST.get('cardiology'))
    if 'dentist' in request.POST:
        clinics.append(request.POST.get('dentist'))
    if 'orthopedic' in request.POST:
        clinics.append(request.POST.get('orthopedic'))
    if 'dermatology' in request.POST:
        clinics.append(request.POST.get('dermatology'))
    chronic_conditions = request.POST.get('chronic_conditions')
    file_path = request.POST.get('file_path')
    if not os.path.isfile(file_path) and '.csv' not in file_path:
        raise FileNotFoundError('No such a csv file')

    patient = [first_name, last_name, pesel, ', '.join(clinics), chronic_conditions]

    with open(file_path, mode='a', newline="") as record_file:
        record_file = csv.writer(record_file, delimiter=',', quotechar='"')
        record_file.writerow(patient)
    return


def open_patient(request):
    return render(request, 'medrecord/open_patient.html')


def opened_record(request):
    print(request)
    if request.method == 'POST':
        try:
            file_path = request.POST.get('file_path')
            print('file_path')
            print(file_path)
            if not os.path.isfile(file_path) and '.csv' not in file_path:
                raise FileNotFoundError('Incorrect csv file name')

            with open(file_path, mode='r') as record_file:
                record_file = csv.reader(record_file, delimiter=',', quotechar='"')
                record = []
                for row in record_file:
                    print(row)
                    print('row')

                    if row:
                        row_dict = {
                            'first_name': row[0],
                            'last_name': row[1],
                            'pesel': row[2],
                            'clinics': row[3],
                            'chronic_conditions': row[4]
                        }
                    record.append(row_dict)
            return render(request, 'medrecord/opened_record.html', {'record': record})
        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/open_patient.html')

    return render(request, 'medrecord/opened_record.html')
