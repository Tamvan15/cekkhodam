from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adu/', views.adu_khodam, name='adu_khodam'),
    path('login/', views.login_view, name='login'),
    path('crud/', views.crud_view, name='crud'),
    path('create_khodam/', views.create_khodam, name='create_khodam'),
    path('update_khodam/<int:id>/', views.update_khodam, name='update_khodam'),
    path('delete_khodam/<int:id>/', views.delete_khodam, name='delete_khodam'),
    path('logout/', views.logout_view, name='logout'),
    path('upload_screenshot', views.upload_screenshot, name='upload_screenshot'),
]
