from django.urls import path

from . import views

app_name = 'medrecord'
urlpatterns = [
    path('', views.index, name='index'),
    path('save_patient/', views.save_patient, name='save_patient'),
    path('open_record/', views.open_record, name='open_record'),
    path('delete/<int:id>/', views.delete, name='delete'),
]
