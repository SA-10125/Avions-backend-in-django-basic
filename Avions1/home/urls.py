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
    path('blogs/',views.render_blogs,name='blogs'),
    path('blogs/read/<str:pk>/',views.read_blog,name='read_blog'),
    path('blogs/new/',views.write_blog,name='new_blog'),
    path('blogs/edit/<str:pk>/',views.edit_blog,name='edit_blog'),
    path('blogs/delete/<str:pk>/',views.delete_blog,name='delete_blog'),
]
