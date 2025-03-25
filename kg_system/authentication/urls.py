from django.contrib import admin
from django.urls import path
from .views import register, login, kg_graph, kg_search

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('kg/graph/', kg_graph, name='kg_graph'),
    path('kg/search/', kg_search, name='kg_search'),
    # path('admin/', admin.site.urls),
]
