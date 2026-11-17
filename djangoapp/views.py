"""Views for the djangoapp API."""
import json
from django.shortcuts import render, redirect
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
    """Log out the current user and return empty userName."""
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"userName": ""}, status=200)

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

def get_dealers(request):
    """Return all dealers."""
    dealers = Dealer.objects.all()
    dealers_data = []
    for d in dealers:
        dealers_data.append({
            "id": d.id,
            "full_name": d.full_name,
            "city": d.city,
            "address": d.address,
            "zip": d.zip,
            "state": d.state,
            "phone": d.phone,
            "email": d.email,
        })
    return JsonResponse({"status": 200, "dealers": dealers_data})

def get_dealer_by_id(request, dealer_id):
    """Return details of one dealer by id."""
    try:
        d = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)

    return JsonResponse({
        "status": 200,
        "dealer": {
            "id": d.id,
            "full_name": d.full_name,
            "short_name": d.short_name,
            "city": d.city,
            "address": d.address,
            "zip": d.zip,
            "state": d.state,
            "lat": d.lat,
            "long": d.long,
            "phone": d.phone,
            "email": d.email,
        },
    })

def get_dealers_by_state(request, state):
    """Return dealers located in the given state."""
    dealers = Dealer.objects.filter(state__iexact=state)
    dealers_data = []
    for d in dealers:
        dealers_data.append({
            "id": d.id,
            "full_name": d.full_name,
            "city": d.city,
            "address": d.address,
            "zip": d.zip,
            "state": d.state,
            "phone": d.phone,
            "email": d.email,
        })
    return JsonResponse({"status": 200, "state": state, "dealers": dealers_data})

from .models import CarMake, CarModel


def get_cars(request):
    """Return all car models with their makes."""
    models_list = []
    for m in CarModel.objects.select_related('car_make').all():
        models_list.append({
            "CarModel": m.name,
            "CarMake": m.car_make.name,
            "type": m.type,
            "year": m.year,
        })
    return JsonResponse({"status": 200, "CarModels": models_list})

def analyze_review(request, text):
    """Return sentiment for the given review text (keyword-based)."""
    positive_words = ['fantastic', 'great', 'good', 'excellent', 'amazing', 'love', 'wonderful', 'best']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'poor', 'horrible', 'disappointing']

    lower = text.lower()
    pos_count = sum(1 for w in positive_words if w in lower)
    neg_count = sum(1 for w in negative_words if w in lower)

    if pos_count > neg_count:
        sentiment = 'positive'
    elif neg_count > pos_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return JsonResponse({
        "status": 200,
        "text": text,
        "sentiment": sentiment,
    })

def dealer_detail_page(request, dealer_id):
    """Render dealer details with reviews."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return render(request, 'djangoapp/dealer_not_found.html', status=404)

    reviews = Review.objects.filter(dealer=dealer)
    return render(request, 'djangoapp/dealer_detail.html', {
        'dealer': dealer,
        'reviews': reviews,
    })

def add_review_page(request, dealer_id):
    """Render review form (GET) or save review (POST)."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return render(request, 'djangoapp/dealer_not_found.html', status=404)

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip() or request.user.username
        review_text = request.POST.get('review', '').strip()
        car_make = request.POST.get('car_make', '').strip()
        car_model = request.POST.get('car_model', '').strip()

        if review_text:
            Review.objects.create(
                dealer=dealer,
                user_name=user_name,
                review=review_text,
                sentiment='positive',
                car_make=car_make,
                car_model=car_model,
            )
            return redirect(f'/djangoapp/dealer/{dealer.id}/')

    return render(request, 'djangoapp/add_review.html', {'dealer': dealer})

def login_page(request):
    """Render a simple login page and authenticate on POST."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp/')
        return render(request, 'djangoapp/login_page.html', {'error': 'Invalid credentials'})
    return render(request, 'djangoapp/login_page.html')


def logout_page(request):
    """Log the user out and redirect to home."""
    logout(request)
    return redirect('/djangoapp/')

def index(request):
    """Home page listing all dealers."""
    dealers = Dealer.objects.all()
    return render(request, 'djangoapp/index.html', {'dealers': dealers})