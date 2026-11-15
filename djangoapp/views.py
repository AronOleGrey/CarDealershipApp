"""Views for the djangoapp API."""
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_user(request):
    """Authenticate a user and return user info."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response = {
            "userName": username,
            "status": "Authenticated"
        }
        return JsonResponse(response, status=200)
    return JsonResponse({"userName": username, "status": "Failed"}, status=401)


@csrf_exempt
def logout_user(request):
    """Log out the current user."""
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"userName": request.user.username, "status": "Logged out"}, status=200)
    return JsonResponse({"status": "Not logged in"}, status=401)

from .models import Dealer, Review


def get_dealer_reviews(request, dealer_id):
    """Return all reviews for the given dealer id."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)

    reviews = Review.objects.filter(dealer=dealer)
    reviews_data = []
    for r in reviews:
        reviews_data.append({
            "id": r.id,
            "user_name": r.user_name,
            "review": r.review,
            "sentiment": r.sentiment,
            "purchase_date": r.purchase_date.isoformat() if r.purchase_date else None,
            "car_make": r.car_make,
            "car_model": r.car_model,
        })

    return JsonResponse({
        "status": 200,
        "dealer": dealer.full_name,
        "reviews": reviews_data,
    })
