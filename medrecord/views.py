from django.contrib import messages
from django.shortcuts import render, redirect

from medrecord.models import Patient


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

            Gets values from POST request, checks if they are correct, saves data to database.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

                Raises
                ------
                ValueError
                    If PESEL length is not 11.

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

    p = Patient(first_name=first_name, last_name=last_name, pesel=pesel, clinics=', '.join(clinics),
                chronic_conditions=chronic_conditions)
    p.save()

    return


def open_record(request):
    """Displays all patients from database.

            Gets all Patient model objects and send then in context to display in table.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

                Returns
                -------
                    render
                        Result of rendering medrecord/open_record.html with patients data in context
    """
    patients = Patient.objects.all()
    return render(request, 'medrecord/open_record.html', {'patients': patients})


def delete(request, id):
    """Removes patient by their id.

            Gets Patient model object by id and deletes it, then redirects to /medrecord/open_record.

                Parameters
                ----------
                request: WSGIRequest
                    Request.
                id: int
                    Patient's id.

                Returns
                -------
                redirect
                    Redirecting to  medrecord/open_record.html
    """
    patient = Patient.objects.get(id=id)
    patient.delete()
    return redirect("/medrecord/open_record")
