from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect

from medrecord.models import Patient


def index(request):
    """Clears session and renders 'medrecord/index.html'.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

    """
    clear_session(request)
    return render(request, 'medrecord/index.html')


def open_record(request):
    """Clears session and displays all patients from database.

            Clears session data. Gets all Patient model objects and send then in context to display in table.

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
                    Redirecting to  /medrecord/open_record
    """
    try:
        patient = Patient.objects.get(id=id)
        patient.delete()
    except ObjectDoesNotExist:
        pass
    return redirect("/medrecord/open_record")


def personal_info(request):
    """Renders 'medrecord/personal_info.html'.

            Parameters
            ----------
            request: WSGIRequest
                Request.

    """
    return render(request, 'medrecord/personal_info.html')


def check_personal_info(request):
    """Checks if first name, last name i pesel are correct.

            Gets values from POST request, checks if they are correct, saves data in session.

            Parameters
            ----------
            request: WSGIRequest
                Request.

            Raises
            ------
            ValueError
                If PESEL length is not 11.

            Returns
            -------
            redirect
                Result of redirect to /medrecord/clinics.
    """
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            print('first_name')
            print(first_name)
            last_name = request.POST.get('last_name')
            pesel = request.POST.get('pesel')
            if len(pesel) != 11:
                raise ValueError("PESEL length must be 11")
        except ValueError as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/personal_info.html')

    request.session['first_name'] = first_name
    request.session['last_name'] = last_name
    request.session['pesel'] = pesel

    return redirect('/medrecord/clinics')


def clinics(request):
    """Renders 'medrecord/clinics.html'.

            Parameters
            ----------
            request: WSGIRequest
                Request.

    """
    return render(request, 'medrecord/clinics.html')


def check_clinics(request):
    """Checks if clinics input is correct.

            Gets values from checked clinics. Converts read values into string and saves in session.

            Parameters
            ----------
            request: WSGIRequest
                Request.

            Raises
            ------
            ValueError
                If PESEL length is not 11.

            Returns
            -------
            redirect
                Result of redirect to medrecord:chronic_conditions.
    """

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
        except ValueError as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/clinics.html')

    return redirect('medrecord:chronic_conditions')


def chronic_conditions(request):
    """Renders 'medrecord/chronic_conditions.html'.

                Parameters
                ----------
                request: WSGIRequest
                    Request.

    """
    return render(request, 'medrecord/chronic_conditions.html')


def check_chronic_conditions(request):
    """Checks if chronic conditions input is correct.

            Checks if chronic conditions input is correct. Then saves it to session data.

            Parameters
            ----------
            request: WSGIRequest
                Request.

            Raises
            ------
            ValueError
                If chronic conditions length is more than 1000.

            Returns
            -------
            redirect
                Result of redirect to medrecord:save_data.
    """
    if request.method == "POST":
        try:
            chronic_conditions = request.POST.get('chronic_conditions')
            if len(chronic_conditions) > 1000:
                raise ValueError("Chronic conditions must be shorter than 1000 characters")
            request.session['chronic_conditions'] = chronic_conditions

        except ValueError as ex:
            messages.error(request, ex)
            return render(request, 'medrecord/chronic_conditions.html')

    return redirect('medrecord:save_data')


def save_data(request):
    """Saves patient to database.

        Creates Patient model object from session data. Then saves object to database.

        Parameters
        ----------
        request: WSGIRequest
            Request.

        Returns
        -------
        redirect
            Result of redirect to medrecord:open_record.
    """
    p = Patient(first_name=request.session.get('first_name'), last_name=request.session.get('last_name'),
                pesel=request.session.get('pesel'), clinics=request.session.get('clinics'),
                chronic_conditions=request.session.get('chronic_conditions'))
    try:
        p.save()
    except IntegrityError as e:
        messages.error(request, e)

    return redirect('medrecord:open_record')


def clear_session(request):
    """Clears session data.

            Removes values for all keys in session.

            Parameters
            ----------
            request: WSGIRequest
                Request.

    """

    for key in list(request.session.keys()):
        del request.session[key]

    return
