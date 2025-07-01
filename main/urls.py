from django.urls import path, include
from django.contrib import admin
from . import views, dashboard_views

app_name = 'main'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Services
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Team
    path('team/', views.team, name='team'),
    
    # Projects
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # News
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    
    # About
    path('about/', views.about, name='about'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # AJAX endpoints
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Admin dashboard
    path('admin/dashboard-stats/', dashboard_views.dashboard_stats, name='dashboard_stats'),
]
