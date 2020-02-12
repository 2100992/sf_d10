from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name='index_url'),
    path('model/', views.CarModelListView.as_view(), name='car_models_list_url'),
    path('model/<slug:slug>/', views.CarModelDetailView.as_view(), name='car_model_url'),
    path('maker/', views.CarMakerListView.as_view(), name='car_makers_list_url'),
    path('maker/<slug:slug>/', views.CarMakerDetailView.as_view(), name='car_maker_url'),
]
