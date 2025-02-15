from django.urls import path
from . import views 
from .views import login_view, signup_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('', views.landing_page, name='landing_page'), 
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home'),  
    path('best-arbitrage/', views.best_arbitrage_view, name='best_arbitrage'), 
    path('chat/', views.chat_view, name='chat'),
]
