from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('results', views.get_results, name='results'),
    path('add_approved_menu/<str:calories>/<str:bzu>/<str:genome>', views.add_approved_menu, name='add_approved_menu'),\
    path('approved_menues', views.show_approved_menues, name='approved_menues'),
]