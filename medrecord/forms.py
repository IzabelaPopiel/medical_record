from django.contrib.auth.forms import UserCreationForm
from django.forms import forms

from medrecord.models import Patient


class PatientForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'pesel', 'clinics', 'chronic_conditions')


class PersonalInfo(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    pesel = forms.CharField(max_length=11)


CLINICS = (
    ("cardiology", "Cardiology"),
    ("dentist", "Dentist"),
    ("orthopedic", "Orthopedic"),
    ("dermatology", "Dermatology"),
)


class Clinics(forms.Form):
    clinics = forms.MultipleChoiceField(
        choices=CLINICS,  # this is optional
        widget=forms.CheckboxSelectMultiple,
    )


class ChronicConditions(forms.Form):
    chronic_conditions = forms.CharField(max_length=1000, blank=True, null=True)
