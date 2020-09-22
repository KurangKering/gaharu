from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='gaharu/index'),
    path('data_master/', views.data_master, name='gaharu/data_master'),
    path('proses_input/', views.proses_input, name='gaharu/proses_input'),
    path('data_ekstraksi/', views.data_ekstraksi, name='gaharu/data_ekstraksi'),
    path('data_anfis/', views.data_anfis, name='gaharu/data_anfis'),
    path('proses_anfis/', views.proses_anfis, name='gaharu/proses_anfis'),
    path('klasifikasi/', views.klasifikasi, name='gaharu/klasifikasi'),
    path('pengujian/', views.pengujian, name='gaharu/pengujian'),
]