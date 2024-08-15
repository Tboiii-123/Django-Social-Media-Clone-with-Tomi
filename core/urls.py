
# Importing the path mathod
from django.urls import path
# Importing the view.py file
from . import views

urlpatterns = [
    path('',views.index ,name='index'),
#Signup
    path('signup/',views.signup ,name='signup'),

#login
    path('signin/',views.signin ,name='signin'),

#logout

    path('logout/',views.Logout , name='logout'),


#settings

    path('settings/', views.settings , name='settings'),


#upload

    path('upload/', views.upload , name='upload'),


#like post
    path('like-post/', views.like_post , name='like-post'),

#profile
    path('profile/<str:pk>', views.profile , name='profile'),
    

#follow
    path('follow/', views.follow , name='follow'),



#search
    path('search/', views.search , name='search'),

    
    


]