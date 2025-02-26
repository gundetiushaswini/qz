
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),# Home page
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('quiz/<int:category_id>/', views.quiz, name='quiz'),  # Quiz page
    path('results/<int:category_id>/', views.results, name='results'),  # Results page
    path('leaderboard/', views.leaderboard, name='leaderboard'),  # Leaderboard
    path('contact/', views.contact, name='contact'),  # New URL for Contact
    path('about/', views.about, name='about'), # New URL for About
    path('faq/', views.faq_view, name='faq'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]


