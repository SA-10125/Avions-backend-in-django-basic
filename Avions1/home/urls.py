from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.render_simple_homepage,name='home'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('gallery/',views.render_gallery,name='gallery_page'),
    path('events/',views.render_events,name='events_page'),
    path('contact/',views.render_contact_us,name='contact_us_page'),
    
]
