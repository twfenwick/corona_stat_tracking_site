from django.urls import path

from . import views

# Sets the namespace:
app_name = 'dailystats'

urlpatterns = [
    path('', views.index, name='index')
]
