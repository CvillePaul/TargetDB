from django.urls import path

from . import views

app_name = "tom"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("target/<int:pk>/", views.TargetView, name="target"),
    path("observatory/<int:pk>/", views.ObservatoryView.as_view(), name="observatory"),
    path("observation/<int:pk>/", views.ObservationView.as_view(), name="observation"),
    path("person/<int:pk>/", views.PersonView.as_view(), name="person"),
]
