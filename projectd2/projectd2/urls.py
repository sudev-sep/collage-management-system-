"""
URL configuration for projectd2 project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('register_h/', views.register_h, name='register_h'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_h/', views.admin_h, name='admin_h'),
    path('teacher_h/', views.teacher_h, name='teacher_h'),
    path('teacher_edit/<int:id>/', views.teacher_edit, name='teacher_edit'),
    path('student_h/', views.student_h, name='student_h'),
    path('teacher_admin/', views.teacher_admin, name='teacher_admin'),
    path('delete_t/<int:id>/', views.delete_t, name='delete_t'),
    path('approve_t/<int:id>/', views.approve_teacher, name='approve_t'),
    path('approve_s/<int:id>/', views.approve_student, name='approve_s'),
    path('student_admin/', views.student_admin, name='student_admin'),
    path('delete_s/<int:id>/', views.delete_s, name='delete_s'),
    path('add_department/', views.add_department, name='add_department'),
    path('view_students/', views.view_students, name='view_students'),
    path('notes/<int:id>/', views.notes, name='notes'),
    path('student_edit/<int:id>/', views.student_edit, name='student_edit'),
    path('view_teachers/', views.view_teachers, name='view_teachers'),
    path('view_notes/', views.view_notes, name='view_notes'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
