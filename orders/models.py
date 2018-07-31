from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import validate_comma_separated_integer_list


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Size(models.Model):
    name = models.CharField(max_length=64)
    price = models.PositiveIntegerField

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name="items")
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}"


class Extra(models.Model):
    name = models.CharField(max_length=64)
    categories = models.ManyToManyField(Category, blank=True)
    items = models.ManyToManyField(Item, blank=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, null=True,
        validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["name"]

    def get_categories(self):
        return ", ".join([str(category) for category in self.categories.all()])

    def get_items(self):
        return ", ".join([str(category) for category in self.items.all()])

    def __str__(self):
        return f"{self.name}"


class AddOn(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class ShoppingCart(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.CharField(validators=[validate_comma_separated_integer_list],
                             blank=True, null=True, max_length=256)

    def append_item(self, item_id):
        if self.items != None:
            items_list = self.items.split(",")
            items_list.append(item_id)

            self.items = ",".join(items_list)
        else:
            self.items = item_id

    def get_quantity(self):
        return len(self.items.split(","))

    def get_items(self):
        return self.items
