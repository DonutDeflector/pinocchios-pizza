from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as logout_request
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Category, Item, ShoppingCart

import json

# Create your views here.


def index(request):
    # check to see if user is logged in, redirect to login if not
    authentication_check(request)

    context = {
        "categories": Category.objects.all(),
        "items": Item.objects.all()
    }
    return render(request, "orders/index.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html",
                          {"message": "Invalid credentials."})
    return render(request, "orders/login.html")


def register(request):
    if request.method == "POST":
        # capture form inputs
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        # Capitalize first and last name
        first_name.capitalize()
        last_name.capitalize()

        # if passwords match, proceed; else, inform the user
        if password == confirm_password:
            # if the username is already taken, inform the user
            if User.objects.filter(username=username).exists():
                return render(request, "orders/register.html",
                              {"message": "Username already taken."})
            # if the password is too short, inform the user
            if len(password) < 8:
                return render(request, "orders/register.html",
                              {"message": "Passwords must be at least 8 \
                               characters in length."})
            # register user
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name,
                email=email, password=password)
            user.save()

            # redirect user to login page, display success message
            return render(request, "orders/login.html",
                          {"message": "Successfully registered. Please login."})
        else:
            return render(request, "orders/register.html",
                          {"message": "Passwords don't match."})
    else:
        return render(request, "orders/register.html")


def logout(request):
    logout_request(request)

    return render(request, "orders/login.html", {"message": "Logged out."})


def shopping_cart_items(request):
    """Handles Adding Items to Cart and Getting Quantity of Items in Cart"""

    if request.method == "POST":
        # capture user requesting information
        current_user = request.user

        if len(request.body) == 0:
            # if shopping cart exists for the user, return quantity, else return
            # default value of 0
            if ShoppingCart.objects.filter(username=current_user):
                shopping_cart = ShoppingCart.objects.get(username=current_user)

                # get shopping cart quantity
                shopping_cart_quantity = shopping_cart.get_quantity()

                # return shopping cart quantity
                return JsonResponse({"quantity": shopping_cart_quantity})
            else:
                return JsonResponse({"quantity": "0"})

        # load json from ajax request
        data = json.loads(request.body)

        # if item_id exists, run protocol for added item to cart
        if "item_id" in data:
            # capture item
            item_id = data["item_id"]

            # if a cart exists for the user, find it
            if ShoppingCart.objects.filter(username=current_user):
                shopping_cart = ShoppingCart.objects.get(username=current_user)
            # if not, create cart and add item to the cart
            else:
                shopping_cart = ShoppingCart.objects.create(
                    username=current_user)

            # call function to add item and save it
            shopping_cart.append_item(item_id)
            shopping_cart.save()

            # get shopping cart quantity
            shopping_cart_quantity = shopping_cart.get_quantity()

            return JsonResponse({"quantity": shopping_cart_quantity})

    else:
        return HttpResponse(403)


def shopping_cart(request):
    # check to see if user is logged in, redirect to login if not
    authentication_check(request)

    # fetch current user
    current_user = request.user

    return render(request, "orders/shopping_cart.html")

####################
# helper functions #
####################


def authentication_check(request):
    if not request.user.is_authenticated:
        return redirect("login")
