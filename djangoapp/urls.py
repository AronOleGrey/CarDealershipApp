"""URL patterns for the djangoapp API."""
from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_by_id'),
    path('dealers/<str:state>', views.get_dealers_by_state, name='dealers_by_state'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('analyze/<str:text>', views.analyze_review, name='analyze_review'),
]
