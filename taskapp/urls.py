from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:id>/add_task', views.add_task, name='add_task'),
    path('task/<int:id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:id>/delete/', views.task_delete, name='task_delete'),
    path('project/', views.add_project, name='add_project'),
    path('project/<int:id>', views.project_detail, name='project_detail'),
    path('project/<int:id>/edit', views.project_edit, name='project_edit'),
    path('project/<int:id>/delete', views.project_delete, name='project_delete'),
    path('login/', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # path('my_tasks/<int:id>', views.my_tasks, name='my_tasks'),
    # path('task/<int:task_id>/user/delete/<int:user_id>', views.delete_user_from_task, name='delete_user_from_task'),
    # path('task/<int:id>/user/add/', views.add_user_to_task, name='add_user_to_task'),
    # path('tasks/available/', views.available_tasks, name='available_tasks'),
]
