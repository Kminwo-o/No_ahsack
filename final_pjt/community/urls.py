from django.urls import path

from . import views

app_name = 'community'

urlpatterns = [
    path('detail/', views.detail, name='detail'),
]
