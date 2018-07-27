from django.contrib import admin

from .models import Category, Item, Size, Topping, AddOn

# Register your models here.
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(AddOn)


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "category", "price")
    search_fields = ("name", "category")


admin.site.register(Item, ItemAdmin)
