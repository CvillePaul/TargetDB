from django.urls import path

from . import views

app_name = "tom"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("target/<int:pk>/", views.TargetView, name="target"),
    path("observatory/<int:pk>/", views.ObservatoryView.as_view(), name="observatory"),
    path("person/<int:pk>/", views.PersonView.as_view(), name="person"),
    path("import_targets/", views.ImportTargetsView, name="import_targets"),
]
