from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 리뷰 전체 페이지 [Community]
    path('', views.index, name='index'),
    # 리뷰 작성 페이지 
    path('create/', views.create, name='create'),
    # 리뷰 상세 페이지
    path('<int:review_pk>/', views.detail, name='detail'),
    # 댓글작성 
    path('<int:review_pk>/comments/create/', views.create_comment, name='create_comment'),
    # 리뷰 좋아요
    path('<int:review_pk>/like/', views.like, name='like'),
]
