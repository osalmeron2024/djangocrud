"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from customerrors import views as error_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/signup/', views.signup, name='signup'),
    path('tasks/list_tasks/', views.show_tasks, name='list_tasks'),
    path('tasks/completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:id_task>/', views.show_task_detail, name='task_detail'),
    path('tasks/<int:id_task>/complete_task/',
         views.complete_task, name='complete_task'),
    path('tasks/<int:id_task>/remove_task/',
         views.remove_task, name='remove_task'),
    path('logout/', views.close_session, name='logout'),
    path('tasks/signin/', views.CustomLoginView.as_view(), name='signin'),
    # as_view() Es obligatorio en CBV para que Django convierta la clase en una vista funcional.
]

# Manejo de errores
handler404 = error_views.custom_page_not_found
handler500 = error_views.custom_server_error
