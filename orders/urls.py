from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("shopping_cart_items", views.shopping_cart_items,
         name="shopping_cart_items"),
    path("shopping_cart", views.shopping_cart, name="shopping_cart")
]
