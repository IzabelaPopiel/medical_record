from django.urls import path

from . import views

app_name = 'medrecord'
urlpatterns = [
    path('', views.index, name='index'),
    path('save_patient/', views.save_patient, name='save_patient'),
    path('open_patient/', views.open_patient, name='open_patient'),
]