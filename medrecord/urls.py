from django.urls import path

from . import views

app_name = 'medrecord'
urlpatterns = [
    path('', views.index, name='index'),
    path('save_patient/', views.save_patient, name='save_patient'),
    path('open_file/', views.open_file, name='open_file'),
    path('opened_record/', views.opened_record, name='opened_record'),
]