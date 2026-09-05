from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'checkins'

urlpatterns = [
    # ============================================
    # صفحات اصلی
    # ============================================
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # ============================================
    # ثبت حال
    # ============================================
    path('check-in/', views.check_in, name='check_in'),
    path('get-form/', views.get_form, name='get_form'),
    
    # ============================================
    # گزارش
    # ============================================
    path('report/', views.report, name='report'),
    
    # ============================================
    # احراز هویت
    # ============================================
    path('login/', auth_views.LoginView.as_view(template_name='checkins/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='checkins/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)