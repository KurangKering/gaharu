from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='gaharu/index'),
    path('data_master/', views.data_master, name='gaharu/data_master'),
    path('tambah_data_master/', views.tambah_data_master, name='gaharu/tambah_data_master'),
    path('proses_tambah_data_master/', views.proses_tambah_data_master, name='gaharu/proses_tambah_data_master'),
    path('hapus_data/', views.hapus_data, name='gaharu/hapus_data'),
    path('detail_gambar/', views.detail_gambar, name='gaharu/detail_gambar'),
    path('download_csv/', views.download_csv, name='gaharu/download_csv'),
    path('data_anfis/', views.data_anfis, name='gaharu/data_anfis'),
    path('tambah_model/', views.tambah_model, name='gaharu/tambah_model'),
    path('proses_pelatihan/', views.proses_pelatihan, name='gaharu/proses_pelatihan'),
    path('hapus_anfis/', views.hapus_anfis, name='gaharu/hapus_anfis'),
    path('lihat_anfis/<int:model_id>/', views.lihat_anfis, name='gaharu/lihat_anfis'),
    path('pengujian/', views.pengujian, name='gaharu/pengujian'),
    path('proses_pengujian/', views.proses_pengujian, name='gaharu/proses_pengujian'),
]
