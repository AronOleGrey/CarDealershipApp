"""URL patterns for the djangoapp API and pages."""
from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
path('get_dealers', views.get_dealers, name='get_dealers'),
path('get_cars', views.get_cars, name='get_cars'),
    path('dealer/<int:dealer_id>/', views.dealer_detail_page, name='dealer_detail_page'),
    path('dealer/<int:dealer_id>/review/', views.add_review_page, name='add_review_page'),
    path('api/dealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_by_id'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('dealers/<str:state>', views.get_dealers_by_state, name='dealers_by_state'),
    path('analyze/<str:text>', views.analyze_review, name='analyze_review'),
]