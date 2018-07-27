from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "orders/index.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html",
                          {"message": "Invalid credentials."})
    else:
        return render(request, "orders/login.html")


def logout_request(request):
    logout(request)
    return render(request, "orders/login/html", {"message:" "Logged out."})
