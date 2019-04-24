from django.urls import path
from . import views

app_name = 'main.todo'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path("todos/", views.todo_list, name="todo_list"),
    path("todo", views.todo_create, name="todo_create"),
    path("todo/<int:pk>/", views.todo_update, name="todo_update"),
    path("todo/del/<int:pk>/", views.todo_delete, name="todo_delete"),
]
