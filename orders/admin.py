from django import forms
from django.contrib import admin
from .models import Category, Item, Size, Extra, AddOn, ShoppingCart

# Register your models here.
admin.site.register(Category)
admin.site.register(Size)


class CustomItemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        name = "Name: " + str(obj)
        category = "Category: " + str(obj.category)
        size = "Size: " + str(obj.size)

        item_properties_list = [name, category, size]
        item_properties_list = " | ".join(item_properties_list)

        return (item_properties_list)


class ExtraAdminForm(forms.ModelForm):
    items = CustomItemChoiceField(queryset=Item.objects.all())

    class Meta:
        model = Item
        fields = "__all__"


class ExtraAdmin(admin.ModelAdmin):
    list_display = ["name", "get_categories", "get_items", "price"]
    search_fields = ["name"]
    form = ExtraAdminForm


admin.site.register(Extra, ExtraAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "size", "price"]
    search_fields = ["name"]


admin.site.register(Item, ItemAdmin)


class AddOnAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    search_fields = ["name"]


admin.site.register(AddOn, AddOnAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["username"]
    search_fields = ["name"]


admin.site.register(ShoppingCart, ShoppingCartAdmin)
