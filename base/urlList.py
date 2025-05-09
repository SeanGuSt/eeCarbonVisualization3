from django.urls import path
from . import views
app_name = "base"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('stationFinder/', views.IndexView.as_view(), name = "stationFinder"),
    path('detailedStation/', views.DetailedView.as_view(), name = "detailedStation"),
    path('ajax/load-layers/', views.load_layer, name = "ajax_load_layer"),#See views.py
    path('ajax/download-layers/', views.download_layer, name = "ajax_download_layer"),#See views.py
    path('ajax/spline/', views.spline, name = "ajax_spline_layer"),#See views.py
    path('ajax/build_spline/', views.get_spline_line, name = "ajax_spline_line"),
    path('ajax/spline_area/', views.get_spline_area_average, name = "ajax_spline_area"),
    path('ajax/update_pedon/', views.get_pedon_for_radio, name = "ajax_pedon_list"),
    path('ajax/download-splines/', views.download_spline, name = "ajax_download_spline"),#See views.py
]