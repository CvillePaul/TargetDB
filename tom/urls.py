from django.urls import path

from . import views

app_name = "tom"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("target/<int:pk>/", views.TargetView.as_view(), name="target"),
    path("observatory/<int:pk>/", views.ObservatoryView.as_view(), name="observatory"),
    path("observation/<int:pk>/", views.ObservationView, name="observation"),
]
