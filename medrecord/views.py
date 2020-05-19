import csv
import os

from django.contrib import messages
from django.shortcuts import render


def index(request):
    """Renders 'medrecord/index.html'.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

    """
    return render(request, 'medrecord/index.html')


def save_patient(request):
    """Reads and analyze request and saves patient data in csv file.

            Calls saving function with POST request arguement, renders medrecord/save_patient.html
            with info about successful saving data or about error.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

                Returns
                -------
                    render
                        Result of rendering medrecord/save_patient.html.
    """
    if request.method == "POST":
        try:
            save_request_data(request)
            messages.success(request, "Data saved successfully")

        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
    return render(request, 'medrecord/save_patient.html')


def save_request_data(request):
    """Writes patient data to csv file.

            Gets values from POST request, checks if they are correct, writes data to cvs file.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

                Raises
                ------
                ValueError
                    If PESEL length is not 11.
                FileNotFoundError
                    If file not exists or is not .csv.

    """
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
        raise FileNotFoundError('Incorrect csv file name')

    patient = [first_name, last_name, pesel, ', '.join(clinics), chronic_conditions]

    with open(file_path, mode='a', newline="") as record_file:
        record_file = csv.writer(record_file, delimiter=',', quotechar='"')
        record_file.writerow(patient)
    return


def open_file(request):
    """Renders 'medrecord/open_file.html'.

        Parameters
        ----------
        request: WSGIRequest
            Request.

    """
    return render(request, 'medrecord/open_file.html')


def opened_record(request):
    """Reads and analyze request and renders meancalc/result.html with calculated value.

            Gets file path from POST request, checks if it is correct, reads given file,
            saves in structure of list and dictionaries to display data in table.
            If error occurs displays proper information.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

                Raises
                ------
                FileNotFoundError
                    If file not exists or is not .csv.

                Returns
                -------
                    render
                        Result of rendering meancalc/result.html with read data in context
    """
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
            return render(request, 'medrecord/open_file.html')

    return render(request, 'medrecord/opened_record.html')
