from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect

from medrecord.models import Patient


def index(request):
    """Renders 'medrecord/index.html'.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

    """
    clear_session(request)
    return render(request, 'medrecord/index.html')


# def save_patient(request):
#     """Reads and analyze request and saves patient data in csv file.
#
#             Calls saving function with POST request arguement, renders medrecord/personal_info.html
#             with info about successful saving data or about error.
#
#                 Parameters
#                 ----------
#                 request: WSGIRequest
#                     Request.
#
#                 Returns
#                 -------
#                     render
#                         Result of rendering medrecord/personal_info.html.
#     """
#     clear_session(request)
#     if request.method == "POST":
#         try:
#             save_request_data(request)
#             messages.success(request, "Data saved successfully")
#
#         except (ValueError, FileNotFoundError) as ex:
#             messages.error(request, ex)
#     return render(request, 'medrecord/personal_info.html')


# def save_request_data(request):
#     """Writes patient data to csv file.
#
#             Gets values from POST request, checks if they are correct, saves data to database.
#
#                 Parameters
#                 ----------
#                 request: WSGIRequest
#                     Request.
#
#                 Raises
#                 ------
#                 ValueError
#                     If PESEL length is not 11.
#
#     """
#     print(request)
#     first_name = request.POST.get('first_name')
#     last_name = request.POST.get('last_name')
#     pesel = request.POST.get('pesel')
#     if len(pesel) != 11:
#         raise ValueError("PESEL length must be 11")
#     clinics = []
#     if 'cardiology' in request.POST:
#         clinics.append(request.POST.get('cardiology'))
#     if 'dentist' in request.POST:
#         clinics.append(request.POST.get('dentist'))
#     if 'orthopedic' in request.POST:
#         clinics.append(request.POST.get('orthopedic'))
#     if 'dermatology' in request.POST:
#         clinics.append(request.POST.get('dermatology'))
#     chronic_conditions = request.POST.get('chronic_conditions')
#     if len(chronic_conditions) > 1000:
#         raise ValueError("Chronic conditions must be shorter than 1000 characters")
#
#     p = Patient(first_name=first_name, last_name=last_name, pesel=pesel, clinics=', '.join(clinics),
#                 chronic_conditions=chronic_conditions)
#     p.save()
#
#     return


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
    clear_session(request)

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
    try:
        patient = Patient.objects.get(id=id)
        patient.delete()
    except ObjectDoesNotExist:
        pass
    return redirect("/medrecord/open_record")


def personal_info(request):
    return render(request, 'medrecord/personal_info.html')


def check_personal_info(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            print('first_name')
            print(first_name)
            last_name = request.POST.get('last_name')
            pesel = request.POST.get('pesel')
            if len(pesel) != 11:
                raise ValueError("PESEL length must be 11")
        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/personal_info.html')

    request.session['first_name'] = first_name
    request.session['last_name'] = last_name
    request.session['pesel'] = pesel

    return redirect('/medrecord/clinics')


def clinics(request):
    return render(request, 'medrecord/clinics.html')


def check_clinics(request):
    if request.method == "POST":
        try:
            clinics = []
            if 'cardiology' in request.POST:
                clinics.append(request.POST.get('cardiology'))
            if 'dentist' in request.POST:
                clinics.append(request.POST.get('dentist'))
            if 'orthopedic' in request.POST:
                clinics.append(request.POST.get('orthopedic'))
            if 'dermatology' in request.POST:
                clinics.append(request.POST.get('dermatology'))
            clinics = ', '.join(clinics)
            request.session['clinics'] = clinics
        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/clinics.html')

        # return render(request, 'medrecord/clinics.html')
    return redirect('medrecord:chronic_conditions')


def chronic_conditions(request):
    return render(request, 'medrecord/chronic_conditions.html')


def check_chronic_conditions(request):
    if request.method == "POST":
        try:
            chronic_conditions = request.POST.get('chronic_conditions')
            request.session['chronic_conditions'] = chronic_conditions

            if len(chronic_conditions) > 1000:
                raise ValueError("Chronic conditions must be shorter than 1000 characters")

        except (ValueError, FileNotFoundError) as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/chronic_conditions.html')

        # return render(request, 'medrecord/clinics.html')
    return redirect('medrecord:save_data')


def save_data(request):
    # saving data to DB
    p = Patient(first_name=request.session.get('first_name'), last_name=request.session.get('last_name'),
                pesel=request.session.get('pesel'), clinics=request.session.get('clinics'),
                chronic_conditions=request.session.get('chronic_conditions'))
    try:
        p.save()
    except IntegrityError as e:
        messages.error(request, e)

    return redirect('medrecord:open_record')


def clear_session(request):

    for key in list(request.session.keys()):
        del request.session[key]

    return
