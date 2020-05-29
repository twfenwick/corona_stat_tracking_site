from django.urls import path

from . import views

# Sets the namespace:
app_name = 'dailystats'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:state_abrv>/', views.states, name='states'),
    path('<str:state_abrv>/<county>/', views.counties, name='states'),
]
