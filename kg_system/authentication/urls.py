from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('kg/graph/', views.kg_graph, name='kg_graph'),
    path('kg/search/', views.kg_search, name='kg_search')
]