from django.urls import path

from . import views

app_name = 'medrecord'
urlpatterns = [
    path('', views.index, name='index'),
    path('personal_info/', views.personal_info, name='personal_info'),
    path('check_personal_info/', views.check_personal_info, name='check_personal_info'),
    path('clinics/', views.clinics, name='clinics'),
    path('check_clinics/', views.check_clinics, name='check_clinics'),
    path('chronic_conditions/', views.chronic_conditions, name='chronic_conditions'),
    path('check_chronic_conditions/', views.check_chronic_conditions, name='check_chronic_conditions'),
    path('save_data/', views.save_data, name='save_data'),
    path('open_record/', views.open_record, name='open_record'),
    path('delete/<int:id>/', views.delete, name='delete'),
]
