from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # This handles routing for the blog app
    path('accounts/login/', views.LoginView.as_view(), name='login'),  # Correct login view
    path('accounts/logout/', views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),  # Correct logout view
]
