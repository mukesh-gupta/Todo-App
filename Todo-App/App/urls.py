from django.urls import path

from . import views

urlpatterns=[
path('',views.home,name='users'),
    path('index/',views.index,name='index'),
    path('create/',views.create,name='create'),
    path('list/',views.TodoList,name='list'),
path('detail/<pk>',views.TodoDetail,name='detail'),
path('update/<pk>',views.TodoUpdate,name='update'),
path('delete/<pk>',views.TodoDelete,name='delete'),
path('complete/',views.TodoComp,name='complete'),
path('comp/<pk>', views.TodoCopmpleted, name='MartCompleted'),
path('pdf/<pk>',views.todo_pdf,name='pdf'),

]