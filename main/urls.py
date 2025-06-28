from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('team/', views.team_list, name='team_list'),
    path('partners/', views.partners_view, name='partners'),
    path('feasibility/', views.feasibility_view, name='feasibility'),
    path('designs/', views.design_more, name='designs'),
    path('analysis/', views.analysis_more, name='analysis'),
    path('engineering/', views.engineering_more, name='engineering'),
    path('permitting/', views.permitting_more, name='permitting'),
    path('construction/', views.construction_more, name='construction'),
    path('engineering/', views.engineering_more, name='engineering_more'),
]