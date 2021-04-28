from django.urls import path

from . import views

app_name = 'bonapetit'
urlpatterns = [
    path("user", views.UserList.as_view()),
    path("user/<int:pk>", views.UserDetail.as_view()),
    path('authenticate', views.AuthUserLoginView.as_view()),
    path("menu", views.MenuList.as_view()),
    path("menu/<uuid:uuid>", views.MenuDetail.as_view()),
    path("menuoption", views.MenuOptionList.as_view()),
    path("menuoption/<int:id>", views.MenuOptionDetail.as_view()),
    path("employeemenu", views.EmployeeMenuList.as_view()),
    #path('', views.home ),
]
