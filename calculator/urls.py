from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('results', views.get_results, name='results'),
]