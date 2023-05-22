from django.urls import path

from . import views

app_name = 'movies'

urlpatterns = [
    # 로그인 후 기본 페이지
    path('index/', views.index, name="index"),
    # 영화를 클릭했을 시 이동할 detail 페이지
    path('movie_detail/<int:movie_pk>', views.movie_detail, name='detail'),
    path('movie_detail/<int:movie_pk>/like/', views.movie_like, name='like'),
    
]
